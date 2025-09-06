# Career Advisor App Summary for PlantUML

**Overview**: A web app for software engineers to get AI-driven career advice. Users authenticate via AWS Cognito (email/password, LinkedIn OAuth planned), manage profiles (skills, experience, enriched via conversations/LinkedIn), and query Grok AI with premade/custom prompts. Conversations are linear (single thread per conversation), with progressive profile enrichment and RAG for context-aware responses.

## Message Creation & AI Response Flow (with Streaming)

**1. User sends message:**
```
POST /conversations/{conversation_id}/messages
Content-Type: application/json
Accept: text/event-stream
```

**2. Messages Service processes with streaming:**
- Stores user message in database with sequence_number
- **Immediately initiates streaming response** using Server-Sent Events (SSE)
- Returns HTTP 200 with `Content-Type: text/event-stream`

**3. AI Query Process (streaming in real-time):**
- Messages Service → Embeddings Service (embed user query)
- Embeddings Service → pgvector (similarity search for context)
- Messages Service → LLM Service (send query + RAG context)
- **LLM Service → Grok AI (streaming response)**
- **Stream tokens directly to client** as they arrive from Grok AI
- Messages Service buffers complete response for database storage

**4. Stream completion:**
- Messages Service stores complete AI response as new message
- Sends final SSE event with message metadata (message_id, timestamp)
- Closes stream connection

**5. Async background tasks (queued):**
- Extract profile data from user message
- Update user profile via Users Service
- Generate embeddings for the new messages (user + AI messages)

**Result:** User sees AI response tokens appearing in real-time (~200-500ms first token), while complete message storage and profile enrichment happen in the background.

**Microservices**:

- **Users Service**: Manages authentication (Cognito), profile storage (skills, experience_level, years_experience, metadata), enrichment from conversation insights.
  - **Endpoints**:
    - POST /users/{user_id}/register: Sign up via Cognito, store user.
    - POST /users/{user_id}/login: Authenticate via Cognito, return JWT.
    - GET /users/{user_id}/profile: Fetch profile (skills, experience).
    - PUT /users/{user_id}/profile: Update profile manually.
    - POST /users/{user_id}/profile/enrich: Update profile with extracted data (internal).
  - **Queued Tasks**:
    - Profile Update Events: Trigger embeddings service to update profile vectors.
  - **Other Functionalities**:
    - Cognito JWT validation (boto3) for securing endpoints.
    - LinkedIn OAuth (planned) to seed profile data.

- **Conversations Service**: Handles conversation metadata, summaries, and conversation-level operations.
  - **Endpoints**:
    - POST /conversations: Create conversation (Conversation table).
    - GET /users/{user_id}/conversations: List user's conversations.
    - GET /conversations/{conversation_id}: Get conversation details and summary.
    - PUT /conversations/{conversation_id}/summary: Update conversation summary.
  - **Queued Tasks**:
    - Generate Conversation Summary: Every 5 messages, call LLM service to summarize conversation.
  - **Other Functionalities**:
    - Conversation context management for multi-turn interactions.
    - Integration with messages service for conversation flow.

- **Messages Service**: Handles individual message storage, retrieval, and sequential ordering within conversations.
  - **Endpoints**:
    - POST /conversations/{conversation_id}/messages: Save user message, trigger processing.
    - GET /conversations/{conversation_id}/messages: Retrieve conversation messages.
    - GET /messages/{message_id}: Get specific message details.
    - POST /conversations/{conversation_id}/ai-query: Process user query with RAG context.
  - **Queued Tasks**:
    - Extract Profile Data: Call LLM service to extract skills/experience from message.
    - Profile Enrichment: Call Users Service's /profile/enrich to update user profile.
    - Embed Message Text: Call embeddings service to generate and store message vectors.
  - **Other Functionalities**:
    - Sequential message ordering with sequence_number.
    - Integration with embeddings service for RAG queries.
    - Message metadata and type management.

- **Prompts Service**: Stores/retrieves premade prompts for AI queries and manages custom user prompts.
  - **Endpoints**:
    - GET /prompts: List premade prompts (e.g., "Career Paths", "Skill Gaps").
    - GET /prompts/{id}: Get specific prompt template.
    - POST /users/{user_id}/prompts: Create custom user prompt.
    - GET /users/{user_id}/prompts: List user's custom prompts.
  - **Queued Tasks**: None.
  - **Other Functionalities**:
    - Prompt categorization and tagging.
    - Usage analytics and effectiveness tracking.

- **LLM Service**: Handles Grok AI integration, response processing, and context management.
  - **Endpoints**:
    - POST /llm/generate: Generate AI response with context (internal).
    - POST /llm/extract-profile: Extract profile data from text (internal).
    - POST /llm/summarize: Generate conversation summary (internal).
  - **Queued Tasks**: None (processes requests synchronously).
  - **Other Functionalities**:
    - Grok AI API communication and rate limiting.
    - Context injection from RAG system.
    - Response post-processing and validation.
    - API key management via AWS Secrets Manager.

- **Embeddings Service**: Generates vector embeddings and performs similarity search for RAG implementation.
  - **Endpoints**:
    - POST /embeddings/generate: Generate embeddings for text (internal).
    - POST /embeddings/search: Perform similarity search for RAG (internal).
    - POST /embeddings/batch: Batch process existing content.
  - **Queued Tasks**:
    - Embed Profile Updates: Generate and store profile embeddings.
    - Embed Message Text: Chunk message, generate embeddings, store in database.
  - **Other Functionalities**:
    - sentence-transformers integration for embedding generation.
    - pgvector similarity search optimization.
    - Batch processing for existing content migration.

**Database (PostgreSQL with pgvector)**:
- **users**: id (PK, UUID), cognito_user_id (String, unique), email (String, unique), skills (JSONB), experience_level (String: Junior/Mid/Senior), years_experience (Integer), metadata (JSONB), created_at (DateTime), updated_at (DateTime).
- **conversations**: id (PK, UUID), user_id (FK to users), title (String), summary (Text), created_at (DateTime), updated_at (DateTime).
- **messages**: id (PK, UUID), conversation_id (FK to conversations), user_id (FK to users), content (Text), message_type (String: user/assistant/system), sequence_number (Integer), metadata (JSONB), embedding (Vector[384]), created_at (DateTime).
- **prompts**: id (PK, UUID), title (String), content (Text), category (String), is_premade (Boolean), user_id (FK to users, nullable), tags (JSONB), usage_count (Integer), created_at (DateTime), updated_at (DateTime).
- **embeddings**: id (PK, UUID), vector (Vector[384]), metadata (JSONB, e.g., {'type': 'user_message'/'profile', 'chunk_id': 1}), user_id (FK to users), message_id (FK to messages, nullable), conversation_id (FK to conversations, nullable), created_at (DateTime).

**Deployment**:
- Dev: Kubernetes (Tilt + Colima) + PostgreSQL pod.
- Prod: AWS EKS + Fargate + RDS (PostgreSQL) + S3 + CloudFront + API Gateway.
- Secrets: AWS Secrets Manager for Grok API key, DB credentials.

**Data Flows**:
- User logs in (Cognito → Users Service), gets JWT.
- Creates conversation (Conversations Service), sends messages (Messages Service).
- Message triggers profile extraction (Messages Service → LLM Service → Users Service).
- AI query uses RAG (Messages Service → Embeddings Service → LLM Service → Grok AI).
- Embeddings generated asynchronously (Embeddings Service → pgvector storage).
- Frontend (React, Tailwind) displays conversations/messages/responses via API Gateway.
