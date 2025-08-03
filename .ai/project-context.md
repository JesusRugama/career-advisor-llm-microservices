# AI Project Context Template

## Project Overview
**Name**: Career Advisor
**Type**: Web App
**Primary Language**: Typescript/Python
**Framework**: React/FastApi
**Build Tool**: Vite/webpack
**Description**: We are building a AI chat like application that helps software engineers find the best career path for them based on their skills, experience, and interests. The application stored the user's skills, experience, and interests in a database and uses AI to provide personalized career advice. We also provide some premade prompts to help the user get started. For now lets build the app for a single user. Which means no authentication is needed, use the skills from .ai/developer-profiles/ for the user skills.

## Architecture
### Data Flow
- **Database**: undefined
- **External APIs**: x.ai
- **State Management**: undefined
- **Authentication**: undefined

### Key Patterns
- **Caching**: undefined
- **Error Handling**: undefined
- **Logging**: undefined
- **Testing**: undefined

### Directory Structure
```
backend/ #FastApi API
frontend/ #React Frontend
```

## Technology Stack
### Frontend
- **Framework**: React
- **Styling**: Tailwind
- **State**: Zustand
- **Build**: Vite
- **Other Libraries**: Prettier, ESLint

### Backend
- **Runtime**: Python
- **Framework**: FastApi
- **Database**: PostgreSQL
- **ORM**: undefined

### DevOps
- **Hosting**: AWS
- **CI/CD**: GitHub Actions
- **Monitoring**: undefined

## Team Preferences
- **Architecture Philosophy**: Quick and simple solutions
- **Performance vs Maintainability**: Maintainability
- **Risk Tolerance**: balanced

## Development Workflow
- **Branch Strategy**: None (Merge to main)
- **Code Review Process**: None, single dev
- **Testing Requirements**:
- **Deployment Process**: github actions / terraform
