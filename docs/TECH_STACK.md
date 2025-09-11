# Technology Stack

## Backend Technologies

### Core Framework
- **FastAPI 0.116.1** - Modern, fast web framework for building APIs with Python
  - Automatic API documentation generation (OpenAPI/Swagger)
  - Built-in data validation with Pydantic
  - Async/await support for high performance
  - Type hints for better code quality

### Database & ORM
- **PostgreSQL 15** - Primary database with advanced features
  - **pgvector extension** - Vector similarity search for RAG implementation
  - JSONB support for flexible metadata storage
  - Full-text search capabilities
- **SQLAlchemy 2.0.25** - Modern Python ORM
  - Async support with asyncpg
  - Declarative models
  - Advanced query capabilities
- **Alembic 1.13.1** - Database migration tool
  - Version control for database schema
  - Automatic migration generation
- **asyncpg 0.29.0** - High-performance PostgreSQL adapter

### AI & Machine Learning
- **Grok AI API** - Primary LLM provider for career advice
  - Natural language processing
  - Conversation generation
  - Career guidance responses
- **sentence-transformers** - Text embedding generation
  - Semantic similarity search
  - Vector representations for RAG
  - Integration with pgvector

### Authentication & Security
- **AWS Cognito** - User authentication and management
  - Email/password authentication
  - User pool management
  - JWT token handling
- **AWS Secrets Manager** - Secure API key storage
  - Grok AI API key management
  - Database credentials (production)

### Development & Testing
- **pytest 8.4.1** - Testing framework
  - Async test support with pytest-asyncio
  - Comprehensive test coverage
- **FastAPI CLI 0.0.8** - Development server
- **uvicorn 0.35.0** - ASGI server
- **httpx 0.28.1** - HTTP client for testing and API calls

### Data Validation
- **Pydantic 2.11.7** - Data validation and serialization
  - Type validation
  - JSON schema generation
  - Settings management with pydantic-settings

## Frontend Technologies

### Core Framework
- **React** - Component-based UI framework
  - Modern hooks-based development
  - Component reusability
  - Virtual DOM for performance

### Styling & UI
- **Tailwind CSS** - Utility-first CSS framework
  - Responsive design
  - Custom design system
  - Fast development workflow

### Authentication Integration
- **AWS Cognito SDK** - Frontend authentication
  - User registration/login flows
  - Token management
  - Session handling

## Infrastructure & DevOps

### Container & Orchestration
- **Docker** - Containerization platform
- **Kubernetes** - Container orchestration
  - Service discovery
  - Load balancing
  - Auto-scaling capabilities
- **Colima** - Docker runtime (development)
  - Lightweight alternative to Docker Desktop
  - macOS optimized

### Development Environment
- **Tilt** - Development environment orchestration
  - Live reload for microservices
  - Kubernetes integration
  - Fast development iteration

### Cloud Infrastructure (Production)
- **AWS EKS with Fargate** - Managed Kubernetes service
  - Serverless containers
  - Automatic scaling
  - Serverless container management
- **AWS RDS** - Managed PostgreSQL database
  - Automated backups
  - High availability
  - Performance monitoring
- **AWS S3** - Object storage and frontend hosting
  - File uploads and user data
  - Static website hosting for React frontend
  - Bucket policies for public access
- **AWS CloudFront** - Content delivery network
  - Global edge locations for fast delivery
  - Frontend distribution (S3 origin)
  - Cache optimization for static assets
- **AWS Route 53** - DNS management
  - Custom domain mapping
  - DNS routing to CloudFront distribution
- **AWS API Gateway** - API management
  - Request routing to backend services
  - Rate limiting and throttling
  - API versioning

### Infrastructure as Code
- **Terraform** - Infrastructure provisioning
  - Kubernetes-only deployment strategy
  - Version-controlled infrastructure
  - Multi-environment support

### Production Architecture Diagram
```
Custom Domain (Route 53) → CloudFront → S3 (React Frontend)
            ↓
        API Gateway → EKS (Backend Services)
                                ↓
                        RDS (PostgreSQL)
```

**Frontend Flow**:
- User accesses custom domain
- Route 53 resolves to CloudFront distribution
- CloudFront serves React app from S3 bucket
- Static assets cached globally at edge locations

**Backend Flow**:
- Frontend makes API calls to custom domain/api
- Route 53 routes API requests to API Gateway
- API Gateway forwards to EKS services
- Services connect to RDS PostgreSQL database

## Development Tools

### Code Quality
- **Python Type Hints** - Static type checking
- **Pydantic** - Runtime type validation
- **FastAPI** - Automatic API documentation

### Database Tools
- **psql** - PostgreSQL command-line interface
- **pgAdmin** (optional) - Database administration GUI

### Version Control
- **Git** - Source code management
- **GitHub** - Code hosting and collaboration

## Key Dependencies Summary

```
# Core Backend
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.25
alembic==1.13.1
asyncpg==0.29.0
psycopg2-binary==2.9.9

# Data & Validation
pydantic==2.11.7
pydantic-settings==2.10.1

# AI & ML
sentence-transformers  # Version TBD
boto3  # AWS SDK

# Testing
pytest==8.4.1
pytest-asyncio==1.1.0
httpx==0.28.1

# Development
python-dotenv==1.1.1
watchfiles==1.1.0
```

## Architecture Patterns

### Microservices
- Domain-driven service separation
- Independent deployment and scaling
- Service-to-service communication via HTTP/REST
- Shared database per service group

### API Design
- RESTful API endpoints
- OpenAPI/Swagger documentation
- Consistent error handling
- Standardized response formats

### Data Storage
- PostgreSQL for relational data
- JSONB for flexible metadata
- Vector storage for AI embeddings
- Separate schemas per service

### Security
- JWT-based authentication
- AWS Cognito integration
- API key management via AWS Secrets Manager
- Environment-based configuration

## Performance Considerations

### Database
- Connection pooling with asyncpg
- Indexed queries for performance
- Vector similarity search optimization
- Read replicas for scaling (future)

### API
- Async/await for non-blocking operations
- Response caching strategies
- Rate limiting and throttling
- Efficient serialization with Pydantic

### Infrastructure
- Horizontal scaling with Kubernetes
- Auto-scaling based on metrics
- CDN for static content delivery
- Database connection optimization
