# Career Advisor - AI Project Context

## Project Overview
Career Advisor is a web application for software engineers to get personalized career advice using AI. Users authenticate via AWS Cognito, manage their professional profiles, and interact with Grok AI through premade or custom prompts. The system uses RAG (Retrieval-Augmented Generation) to enhance AI responses with relevant conversation history and profile data.

## Business Features

### Authentication & User Management
- **Primary Auth**: AWS Cognito (email/password registration and login)
- **Planned**: LinkedIn OAuth integration for enhanced profile data
- **User Profiles**: Skills array, experience level, years of experience, metadata (JSONB)
- **Profile Enrichment**: Progressive enhancement from conversation insights and LinkedIn data

### Core Functionality
- **AI Conversations**: Sequential message storage with Grok AI integration
- **Prompt Management**: Premade prompts (e.g., "Suggest career paths", "Identify skill gaps") and custom user prompts
- **Conversation Summaries**: Periodic LLM-generated summaries for long conversations
- **RAG Enhancement**: Vector embeddings of messages and profiles for contextual AI responses

### RAG Implementation
- **Embedding Model**: sentence-transformers for text vectorization
- **Vector Storage**: pgvector extension in PostgreSQL
- **Retrieval**: Top-k similarity search for relevant conversation/profile context
- **AI Integration**: Enhanced Grok AI queries with retrieved context

## Quick Reference

### Tech Stack
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy (see [TECH_STACK.md](TECH_STACK.md))
- **Frontend**: React + Tailwind CSS
- **Infrastructure**: Kubernetes + AWS EKS/Fargate + Terraform
- **AI**: Grok AI + sentence-transformers + pgvector

### Architecture
- **Pattern**: 3-Service Microservices (see [ARCHITECTURE.md](ARCHITECTURE.md))
- **Services**: Users Service (8001), Conversations Service (8002), Prompts Service (8004)
- **Active Service**: prompts-service (Port 8004)
- **Database**: PostgreSQL with pgvector extension

## Development Workflow
- **Primary Tool**: Tilt (`tilt up` to start development environment)
- **Container Runtime**: Colima (preferred over Docker Desktop)
- **Live Reload**: Enabled for active services via Tilt configuration
- **Database Access**: Direct connection via `postgresql://postgres:postgres@127.0.0.1:5432/career_advisor`
- **Testing**: Alembic migrations and test suites configured

## Project Structure
```
backend/
├── k8s/                    # Kubernetes manifests
├── microservices/
│   ├── services/           # Individual microservice implementations
│   └── shared/             # Shared utilities and base classes
├── infrastructure/         # Terraform infrastructure code
├── Tiltfile               # Development environment configuration
└── .dockerignore          # Docker build exclusions
```

## Current Development Status
- **Completed**: Basic microservices setup, database migrations, test suites
- **In Progress**: prompts-service development
- **Planned**: AWS Cognito integration, Grok AI integration, RAG implementation

## Database Configuration
- **Host**: localhost (via Kubernetes port forwarding)
- **Port**: 5432
- **Database**: career_advisor
- **User**: postgres
- **Password**: postgres
- **Extensions**: pgvector (for AI embeddings)

## Notes for AI Assistants
- Target users: Software engineers seeking career guidance
- AI Provider: Grok AI (not OpenAI or Claude)
- Only prompts-service is currently enabled for development
- Use `psql` commands for database operations (MCP servers not configured)
- Tilt provides live reload for fast development iteration
- All services follow similar FastAPI + SQLAlchemy patterns
- Infrastructure is managed through Terraform in the infrastructure/ directory
- Focus on RAG implementation for enhanced AI responses
