# System Architecture

## Overview
Career Advisor follows a consolidated 3-service microservices architecture, optimized for rapid development and deployment while maintaining clear separation of concerns. The system is designed for streaming AI responses, efficient RAG implementation, and scalable user management.

## Microservices Architecture

### Service Breakdown

#### 1. Users Service (Port 8001)
**Responsibility**: User management, authentication, and profile data
- User registration and login workflows via AWS Cognito
- Profile management (skills, experience level, years of experience)
- User metadata storage (JSONB format)
- Profile enrichment from conversation insights
- Profile embedding generation and storage

**Database Schema**:
```sql
users (
  id INTEGER PRIMARY KEY,
  cognito_user_id VARCHAR UNIQUE,
  email VARCHAR UNIQUE,
  password_hash VARCHAR,
  skills ARRAY[VARCHAR],
  experience_level VARCHAR, -- Junior/Mid/Senior
  years_experience INTEGER,
  linkedin_token VARCHAR,
  profile_summary TEXT,
  metadata JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**Key Functions**:
- AWS Cognito JWT validation for securing endpoints
- LinkedIn OAuth integration (planned)
- Profile enrichment from conversation data
- Profile embedding updates via sentence-transformers

#### 2. Conversations Service (Port 8002)
**Responsibility**: Complete conversation management with streaming AI responses
- Linear conversation management (single thread per conversation)
- Message storage and retrieval with sequential ordering
- Real-time AI response streaming via Server-Sent Events (SSE)
- RAG implementation with pgvector similarity search
- Conversation summaries and embeddings generation
- Profile data extraction and enrichment coordination

**Database Schema**:
```sql
conversations (
  id INTEGER PRIMARY KEY,
  title VARCHAR,
  timestamp DATETIME,
  user_id INTEGER REFERENCES users(id)
)

messages (
  id INTEGER PRIMARY KEY,
  text TEXT,
  is_user BOOLEAN,
  timestamp DATETIME,
  extracted_data JSONB,
  conversation_id INTEGER REFERENCES conversations(id)
)

embeddings (
  id INTEGER PRIMARY KEY,
  vector VECTOR[768],
  metadata JSONB, -- {'type': 'user_message'/'profile', 'chunk_id': 1}
  user_id INTEGER REFERENCES users(id),
  message_id INTEGER REFERENCES messages(id), -- nullable
  conversation_id INTEGER REFERENCES conversations(id)
)

conversation_summaries (
  id INTEGER PRIMARY KEY,
  summary_text TEXT,
  timestamp DATETIME,
  vector VECTOR[768],
  conversation_id INTEGER REFERENCES conversations(id)
)
```

**Key Functions**:
- Streaming AI responses using Grok API with SSE
- RAG: Embed queries, retrieve top-5 vectors, combine with profile context
- Message chunking for long texts before embedding
- Conversation summarization every 5 messages
- Profile data extraction and enrichment triggers
- sentence-transformers integration for embeddings
- pgvector similarity search optimization

#### 3. Prompts Service (Port 8004) - **Currently Active**
**Responsibility**: Prompt templates and management
- Premade prompt templates (career paths, skill gaps, etc.)
- Custom user prompt creation and storage
- Prompt categorization and tagging
- Usage analytics and effectiveness tracking

**Database Schema**:
```sql
prompts (
  id INTEGER PRIMARY KEY,
  title VARCHAR,
  content TEXT,
  category VARCHAR,
  is_premade BOOLEAN,
  user_id INTEGER REFERENCES users(id), -- NULL for premade prompts
  tags JSONB,
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

**Key Functions**:
- Prompt template management and retrieval
- Custom prompt creation for users
- Usage tracking and analytics

## Data Flow Architecture

### User Authentication Flow
```
Frontend → AWS Cognito → Users Service → Database
                    ↓
              JWT Token Validation
```

### Conversation Flow (with Streaming)
```
User Input → Frontend → Conversations Service → Grok AI
                           ↓                       ↓
                    RAG Context (pgvector)    Streaming Response
                           ↓                       ↓
                    Vector Storage              Frontend (SSE)
```

### RAG (Retrieval-Augmented Generation) Flow
```
1. User Query → Conversations Service (generate query embedding)
2. Conversations Service → pgvector (similarity search)
3. Retrieved Context → Conversations Service (context injection)
4. Enhanced Query → Grok AI → Streaming Response
```

## Communication Patterns

### Inter-Service Communication
- **Protocol**: HTTP/REST APIs + Server-Sent Events (SSE) for streaming
- **Format**: JSON payloads + SSE for real-time responses
- **Authentication**: Service-to-service JWT tokens
- **Error Handling**: Standardized error responses + stream error events
- **Timeout**: Configurable per service + streaming timeout management
- **Streaming**: SSE for AI response streaming from Conversations Service
- **Queue System**: Celery/Redis for background tasks (profile extraction, embeddings)

### Database Access
- **Pattern**: Shared PostgreSQL database with logical separation
- **Database**: Single PostgreSQL instance with pgvector extension
- **Connections**: Connection pooling with asyncpg
- **Migrations**: Service-specific Alembic migrations
- **Vector Storage**: pgvector for embeddings with optimized indexes

### Event-Driven Architecture (Future)
- **Message Queue**: Consider AWS SQS/SNS for async operations
- **Events**: User profile updates, conversation summaries, embedding updates
- **Benefits**: Decoupled services, better scalability

## Security Architecture

### Authentication & Authorization
- **Primary**: AWS Cognito for user authentication
- **Service-to-Service**: JWT tokens with service-specific claims
- **API Keys**: AWS Secrets Manager for external APIs (Grok AI)
- **Database**: Connection string security via environment variables

### Data Protection
- **Encryption**: TLS for all API communications
- **Database**: Encrypted at rest (AWS RDS encryption)
- **Secrets**: AWS Secrets Manager integration
- **PII Handling**: Secure user data storage and processing

## Deployment Architecture

### Development Environment
```
Tilt → Docker Containers → Kubernetes (local)
  ↓
Colima Runtime → PostgreSQL Pod
```

### Production Environment (AWS)
```
GitHub → CI/CD Pipeline → AWS EKS (Fargate)
                            ↓
                        Kubernetes Pods
                            ↓
                        AWS RDS (PostgreSQL)
```

### Infrastructure Components
- **Compute**: AWS EKS with Fargate (serverless containers)
- **Database**: AWS RDS PostgreSQL with pgvector
- **Storage**: AWS S3 for file uploads and static assets
- **CDN**: AWS CloudFront for content delivery
- **API Gateway**: AWS API Gateway for external API management
- **Load Balancing**: Kubernetes ingress controllers

## Scalability Considerations

### Horizontal Scaling
- **Stateless Services**: All services designed to be stateless
- **Database Scaling**: Read replicas for query-heavy operations
- **Caching**: Redis for session and frequently accessed data (future)
- **Auto-scaling**: Kubernetes HPA based on CPU/memory metrics

### Performance Optimization
- **Database Indexing**: Optimized indexes for frequent queries
- **Vector Search**: Efficient pgvector index configuration
- **Connection Pooling**: Async connection management
- **Response Caching**: Cache frequently requested data

## Monitoring & Observability

### Logging Strategy
- **Structured Logging**: JSON format for all services
- **Correlation IDs**: Request tracing across services
- **Log Aggregation**: Centralized logging system (future)

### Metrics & Monitoring
- **Application Metrics**: Custom business metrics per service
- **Infrastructure Metrics**: Kubernetes and AWS CloudWatch
- **Health Checks**: Kubernetes liveness and readiness probes
- **Alerting**: Critical error and performance alerts

## Development Workflow

### Service Development
- **Independent Development**: Each service can be developed separately
- **Shared Dependencies**: Common utilities in `microservices/shared/`
- **Testing Strategy**: Unit tests per service, integration tests for workflows
- **API Documentation**: Auto-generated OpenAPI specs per service

### Database Management
- **Schema Evolution**: Independent migrations per service
- **Data Consistency**: Eventual consistency between services
- **Backup Strategy**: Automated backups with point-in-time recovery

## Future Architecture Enhancements

### Short Term
- **Service Mesh**: Consider Istio for advanced traffic management
- **Caching Layer**: Redis for improved performance
- **Message Queue**: Async processing with AWS SQS

### Long Term
- **Event Sourcing**: For audit trails and data replay capabilities
- **CQRS**: Separate read/write models for complex queries
- **Multi-Region**: Geographic distribution for global users
- **AI Model Hosting**: Self-hosted models for reduced API costs

## API Design Standards

### RESTful Conventions
- **Resource Naming**: Plural nouns for collections
- **HTTP Methods**: Standard CRUD operations
- **Status Codes**: Consistent HTTP status code usage
- **Versioning**: API versioning strategy (/v1/, /v2/)

### Response Format
```json
{
  "data": {...},
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "request_id": "uuid"
  },
  "errors": []
}
```

### Error Handling
- **Consistent Format**: Standardized error response structure
- **Error Codes**: Application-specific error codes
- **Validation Errors**: Detailed field-level validation messages
