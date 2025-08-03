# AI Context Template

A standardized way to provide context to AI assistants about your project and team preferences.

## Quick Start

### For New Projects
1. Copy the `.ai-template/` directory to your project root as `.ai/`
2. Fill out `project-context.md` with your project details
3. Customize `ai-assistant-guide.md` for your team's patterns
4. Team members create individual profiles in `developer-profiles/`
5. Add `.ai/developer-profiles/` to your `.gitignore`

### Directory Structure
```
.ai/
├── project-context.md           # Project architecture & patterns (committed)
├── ai-assistant-guide.md        # Guidelines for AI assistants (committed)
└── developer-profiles/          # Personal preferences (gitignored)
    ├── README.md               # Instructions for team
    ├── template.md             # Template to copy
    └── [developer-name].md     # Individual profiles (private)
```

## Benefits

### For AI Assistants
- **Instant project understanding** - No more guessing at architecture patterns
- **Developer-specific calibration** - Match communication style and technical depth
- **Consistent onboarding** - Same context across different AI tools
- **Avoid common mistakes** - Learn from team's past experiences

### For Development Teams
- **Faster AI onboarding** - New AI tools understand your project immediately
- **Consistent experience** - All team members get similar AI assistance quality
- **Privacy-first** - Personal preferences stay local and private
- **Cross-project portability** - Template works for any technology stack

### For Individual Developers
- **Personalized assistance** - Get explanations at the right technical level
- **Reduced repetition** - Don't re-explain preferences to each AI tool
- **Better collaboration** - AI understands your working style
- **Learning support** - AI can focus on areas you want to improve

## Implementation Guide

### Step 1: Project Context
Fill out the project-context.md template with:
- **Architecture overview** - How data flows through your system
- **Technology stack** - Frameworks, databases, deployment tools
- **Performance characteristics** - Known bottlenecks and optimization targets
- **Team preferences** - Coding standards, risk tolerance, priorities
- **Pain points** - Current issues and areas for improvement

### Step 2: AI Guidelines
Customize ai-assistant-guide.md with:
- **Project-specific patterns** - Common architectural approaches
- **Success patterns** - What has worked well for your team
- **Red flags** - Mistakes to avoid or areas not to change
- **Troubleshooting** - Common issues and how to resolve them

### Step 3: Developer Profiles
Team members create individual profiles with:
- **Skill levels** - Honest assessment across different technologies
- **Communication preferences** - How they like to receive feedback
- **Collaboration style** - Automation level, explanation depth, change size
- **Learning goals** - Areas they want to improve or explore

### Step 4: Privacy Setup
The template includes a local `.gitignore` in the `developer-profiles/` directory that automatically protects individual profiles. You can also add this to your project's main `.gitignore` for extra protection:
```
# AI Assistant Context (keep developer profiles private)
.ai/developer-profiles/
```

## Usage Examples

### For AI Assistants
```markdown
Before starting work:
1. Read .ai/project-context.md for architecture understanding
2. Check .ai/developer-profiles/[user].md for individual preferences
3. Follow guidelines in .ai/ai-assistant-guide.md
4. Ask clarifying questions if context is unclear
```

### For Developers
```markdown
When working with a new AI assistant:
1. Point them to the .ai/ directory
2. Let them read your profile and project context
3. Provide feedback on their initial approach
4. Update your profile based on what works/doesn't work
```

## Customization

### Technology-Specific Additions
- **Frontend projects**: Add component patterns, state management approaches
- **Backend projects**: Include API design patterns, database schemas
- **Mobile projects**: Platform-specific considerations, deployment processes
- **DevOps projects**: Infrastructure patterns, monitoring approaches

### Team Culture Adaptations
- **Startup teams**: Emphasize speed and iteration
- **Enterprise teams**: Focus on stability and compliance
- **Open source**: Include contribution guidelines and community patterns
- **Consulting**: Add client-specific considerations and constraints

## Best Practices

### Maintaining Context
- **Regular updates** - Keep project context current as architecture evolves
- **Team reviews** - Periodically review and improve AI guidelines
- **Feedback loops** - Update based on AI assistant performance
- **Version control** - Track changes to understand what works

### Privacy Considerations
- **Sensitive information** - Don't include secrets, credentials, or personal data
- **Team boundaries** - Respect individual privacy preferences
- **Access control** - Consider who should have access to project context
- **Data retention** - Understand how different AI tools handle context data

### Adoption Strategy
- **Start small** - Begin with basic project context and expand
- **Lead by example** - Team leads create profiles first
- **Gather feedback** - Ask team how AI assistance could be improved
- **Iterate** - Refine templates based on actual usage patterns

## Contributing

This template is designed to be:
- **Technology agnostic** - Works for any programming language or framework
- **Team scalable** - Supports individual preferences within team standards
- **Privacy conscious** - Keeps personal information local and secure
- **Continuously improvable** - Easy to update as projects and teams evolve

Share improvements and adaptations with other teams to help standardize AI context across the development community.
