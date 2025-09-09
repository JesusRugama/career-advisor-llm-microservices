# Career Advisor App Summary for PlantUML

**Overview**: A web app for software engineers to get AI-driven career advice. Users authenticate via AWS Cognito (email/password, LinkedIn OAuth planned), manage profiles (skills, experience, enriched via conversations/LinkedIn), and query Grok AI with premade/custom prompts. Conversations are linear (single thread per conversation), with progressive profile enrichment and RAG for context-aware responses. Messages trigger immediate streaming AI responses via Grok API.

**Microservices**:

- **User Service**: Manages authentication (Cognito), profile storage (skills, experience_level, years_experience, metadata), enrichment from conversations/LinkedIn.
  - **Endpoints**:
    - POST /customers/{user_id}/register: Sign up via Cognito, store user.
    - POST /customers/{user_id}/login: Authenticate via Cognito, return JWT.
    - GET /customers/{user_id}/profile: Fetch profile (skills, experience).
    - PUT /customers/{user_id}/profile: Update profile manually.
    - POST /customers/{user_id}/profile/enrich: Update profile with extracted data (internal).
  - **Queued Tasks**:
    - Embed Profile Updates: On profile update, embed profile text (sentence-transformers), insert into Embedding (type='profile').
  - **Other Functionalities**:
    - Cognito JWT validation (boto3) for securing endpoints.
    - LinkedIn OAuth (planned) to seed profile data.

- **Conversations Service**: Handles linear conversations, messages, embeddings (sentence-transformers, pgvector), summaries, and RAG-augmented Grok queries with streaming responses.
  - **Endpoints**:
    - POST /customers/{user_id}/conversations: Create conversation (Conversation table).
    - GET /customers/{user_id}/conversations: List user’s conversations.
    - POST /customers/{user_id}/conversations/{conversation_id}/messages: Save user message, embed query, fetch RAG context, stream Grok response via SSE, save response, trigger queued tasks.
    - GET /customers/{user_id}/conversations/{conversation_id}/messages: Retrieve conversation messages.
    - POST /customers/{user_id}/conversations/{conversation_id}/ai-query: Embed query, fetch top-5 embeddings, combine with profile_summary, stream Grok response via SSE, save response.
  - **Queued Tasks**:
    - Extract Profile Data: Call Grok to extract skills/experience from message, store in Message.extracted_data (JSONB).
    - Profile Enrichment: Call User Service’s /profile/enrich to update User table.
    - Generate Conversation Summary: Every 5 messages, call Grok to summarize conversation, embed, store in ConversationSummary.
    - Embed Message Text: Chunk message, embed chunks, insert into Embedding.
  - **Other Functionalities**:
    - RAG: Embed query, retrieve top-5 vectors (pgvector, filter user_id), combine with profile_summary for Grok context.
    - Message chunking for long texts before embedding.
    - Server-Sent Events (SSE) for streaming Grok responses.

- **Prompts Service**: Stores/retrieves premade prompts for AI queries.
  - **Endpoints**:
    - GET /prompts: List premade prompts (e.g., "Career Paths", "Skill Gaps").
    - GET /prompts/{id}: Get specific prompt template.
  - **Queued Tasks**: None.
  - **Other Functionalities**: None.

**Database (PostgreSQL with pgvector)**:
- **User**: id (PK, Integer), email (String, unique), password_hash (String), skills (ARRAY[String]), experience_level (String: Junior/Mid/Senior), years_experience (Integer), linkedin_token (String), profile_summary (Text), metadata (JSONB).
- **Conversation**: id (PK, Integer), title (String), timestamp (DateTime), user_id (FK to User).
- **Message**: id (PK, Integer), text (Text), is_user (Boolean), timestamp (DateTime), extracted_data (JSONB), conversation_id (FK to Conversation).
- **Embedding**: id (PK, Integer), vector (Vector[768]), metadata (JSONB, e.g., {'type': 'user_message'/'profile', 'chunk_id': 1}), user_id (FK to User), message_id (FK to Message, nullable), conversation_id (FK to Conversation).
- **ConversationSummary**: id (PK, Integer), summary_text (Text), timestamp (DateTime), vector (Vector[768]), conversation_id (FK to Conversation).

**Message Creation & AI Response Flow**:
1. **User sends message**:
   - POST /customers/{user_id}/conversations/{conversation_id}/messages
2. **Conversations Service processes synchronously**:
   - Saves message (Message table, text, is_user=True, conversation_id).
   - Embeds query (sentence-transformers), fetches top-5 embeddings (pgvector, filter user_id), retrieves User.profile_summary.
   - Calls Grok API (stream=True), streams response to frontend via Server-Sent Events (SSE).
   - Saves AI response (Message table, is_user=False).
   - Returns StreamingResponse with AI tokens.
3. **Async background tasks (queued via Celery/Redis)**:
   - Extract Profile Data: Call Grok to extract skills/experience, store in Message.extracted_data.
   - Profile Enrichment: Call User Service’s /profile/enrich to update User table.
   - Embed Message Text: Chunk message, embed chunks, insert into Embedding.
   - Generate Conversation Summary (if 5th message): Call Grok to summarize, embed, store in ConversationSummary.
4. **Optional AI query**:
   - POST /customers/{user_id}/conversations/{conversation_id}/ai-query
   - Same as above: embed query, fetch RAG context, stream Grok response via SSE, save response.
5. **Result**: Users get immediate streaming AI responses after sending messages, with enrichment/embeddings handled asynchronously for performance.

**Deployment**:
- Dev: EC2+docker-compose+RDS (PostgreSQL).
- Prod: EKS+Fargate+RDS+S3+CloudFront+API Gateway.
- Secrets: AWS Secrets Manager for Grok API key, DB creds.

**Data Flows**:
- User logs in (Cognito → User Service), gets JWT.
- Sends message (Conversations Service), gets streamed AI response.
- Message triggers queued extraction/enrichment (Grok → User Service).
- Optional AI query streams response (RAG + Grok).
- Frontend (React, Tailwind) displays messages/responses via SSE (S3+CloudFront).