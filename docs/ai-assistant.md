# AI Assistant Enhancement Guide

## Overview
This document outlines recommendations for improving AI assistant effectiveness when working on the Career Advisor project. These suggestions are based on investigation into MCP servers and development workflow optimization.

## Recommended Tools & Integrations

### Database Operations
**Current State**: Using `psql` CLI commands through terminal
**Recommended**: PostgreSQL MCP Server (when available)
- **Benefits**: Direct SQL query execution, structured results, better error handling
- **Alternative**: Continue with `psql` commands until MCP support improves
- **Connection String**: `postgresql://postgres:postgres@127.0.0.1:5432/career_advisor`

### Kubernetes Management
**Recommended**: Kubernetes MCP Server
- **Benefits**: Enhanced `kubectl` operations, pod log access, resource management
- **Current Workaround**: Use terminal commands with `kubectl`
- **Use Cases**: Pod debugging, service status checks, resource scaling

### Infrastructure Management
**Recommended**: Terraform MCP Server
- **Benefits**: Infrastructure state inspection, plan validation, resource management
- **Current Setup**: Manual Terraform commands in `infrastructure/` directory
- **Focus**: Production EKS deployment strategy

### Project Management
**Recommended**: Trello or GitHub Issues MCP Server
- **Benefits**: Ticket creation from code TODOs, development progress sync
- **Workflow**: Create boards for Backlog, Sprint, In Progress, Review, Done
- **Labels**: Bug, Feature, Infrastructure, Documentation
- **Integration**: Auto-create tickets from code comments, sync completion status

### Development Tools
**Recommended**: Git MCP Server
- **Benefits**: Advanced git operations, branch management, commit analysis
- **Use Cases**: Code review assistance, merge conflict resolution, branch strategy

**Recommended**: FastAPI/OpenAPI MCP Server
- **Benefits**: API documentation integration, endpoint testing
- **Use Cases**: Schema validation, API client generation

## Project Documentation Strategy

### Essential Documentation Files
1. **docs/project-context.md** ✅ - Comprehensive project overview for AI context
2. **docs/ai-assistant.md** ✅ - This file - AI enhancement recommendations
3. **docs/TECH_STACK.md** - Detailed technology stack documentation
4. **docs/ARCHITECTURE.md** - Microservices architecture and communication patterns
5. **docs/ROADMAP.md** - MVP features and future enhancements
6. **docs/DEVELOPMENT.md** - Setup instructions, Tilt usage, debugging tips

### Documentation Standards
- **Format**: Markdown for consistency and readability
- **Location**: `docs/` directory for standard convention
- **Maintenance**: Update documentation with each major feature or architectural change
- **AI Context**: Include specific notes for AI assistants in relevant sections

## Development Workflow Enhancements

### Current Workflow
- **Development Environment**: Tilt with Colima
- **Active Service**: prompts-service only
- **Database Access**: Direct PostgreSQL connection
- **Testing**: Alembic migrations and test suites configured

### Recommended Improvements
1. **Enable Additional Services**: Activate users-service and conversations-service in Tiltfile
2. **Automated Testing**: Integrate test runs with Tilt live reload
3. **Code Quality**: Add linting and formatting tools to development workflow
4. **Documentation Generation**: Auto-generate API docs from FastAPI schemas

## MCP Server Configuration Notes

### Compatibility Issues
- **Windsurf/Cascade**: Limited MCP server support compared to Claude Desktop
- **Configuration Problems**: Connection strings disappear after save
- **Workaround**: Use built-in Windsurf tools and terminal commands

### Future Considerations
- **Claude Desktop**: Consider using for MCP server functionality if needed
- **Alternative Tools**: Explore Windsurf-native extensions for enhanced functionality
- **Manual Processes**: Document manual alternatives for MCP server features

## AI Assistant Guidelines

### Project Context
- **Target Users**: Software engineers seeking career guidance
- **AI Provider**: Grok AI (not OpenAI or Claude)
- **Focus Areas**: RAG implementation, AWS integration, microservices development

### Development Priorities
1. **Current**: Single service development (prompts-service)
2. **Next**: AWS Cognito integration
3. **Future**: Grok AI integration, RAG implementation with sentence-transformers

### Best Practices
- **Database Operations**: Use `psql` commands until MCP servers are available
- **Service Development**: Follow FastAPI + SQLAlchemy patterns established in existing services
- **Infrastructure**: Production-only EKS deployment strategy
- **Testing**: Maintain test coverage for all new features and services

## Troubleshooting Common Issues

### MCP Server Problems
- **Symptom**: Connection strings disappear after save
- **Cause**: Windsurf MCP compatibility limitations
- **Solution**: Use terminal commands and built-in tools

### Development Environment
- **Tilt Issues**: Ensure Colima is running, check port conflicts
- **Database Connection**: Verify PostgreSQL pod is running and port-forwarded
- **Service Debugging**: Use `kubectl logs` for container-level debugging

### Infrastructure
- **Terraform State**: Manage state files carefully, use remote backend for production
- **Kubernetes Resources**: Monitor resource usage, especially in development environment

## Future Enhancements

### Short Term
- Complete prompts-service development
- Enable additional microservices in Tilt
- Implement AWS Cognito authentication

### Medium Term
- Integrate Grok AI API
- Implement RAG with sentence-transformers and pgvector
- Add React frontend with Tailwind CSS

### Long Term
- LinkedIn OAuth integration
- Production deployment on AWS EKS
- Advanced RAG features and conversation summaries

## Conclusion

This document serves as a guide for optimizing AI assistant effectiveness on the Career Advisor project. Regular updates to this documentation will ensure continued improvement in development workflow and AI assistance quality.

For questions or suggestions about AI assistant enhancements, refer to this document and update it as new tools and workflows are discovered.
