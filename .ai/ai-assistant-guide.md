# AI Assistant Guide Template

## Quick Start for New AI Assistants

### 1. Read Project Context First
- Start with `project-context.md` for architecture overview
- Understand the technology stack and main patterns
- Check performance characteristics and known bottlenecks
- Review team preferences and development workflow

### 2. Check Developer Profiles
- Look in `developer-profiles/` for individual team member preferences
- Calibrate your communication style and technical depth accordingly
- Respect automation preferences and collaboration styles
- Note learning preferences and experience levels

### 3. Understand the Codebase
- Trace main data flows and architectural patterns
- Identify key entry points and integration patterns
- Look for existing utilities and helper functions
- Understand testing and deployment processes

## General Principles

### Before Implementing Solutions
- **Understand existing patterns** - Don't reinvent what already works
- **Ask clarifying questions** - Verify assumptions about architecture
- **Check constraints** - Understand what can and cannot be changed
- **Consider team preferences** - Respect established coding styles and philosophies

### Communication Style
- **Match developer preferences** - Some prefer detailed explanations, others want direct solutions
- **Show, don't just tell** - Provide working code examples when possible
- **Be collaborative** - Allow for interruption and course correction
- **Explain trade-offs** - Help teams make informed decisions

### Code Changes
- **Start small** - Make focused changes that can be easily reviewed
- **Build incrementally** - Allow for feedback and iteration
- **Follow existing patterns** - Consistency is often more valuable than perfection
- **Document decisions** - Explain why certain approaches were chosen

## Common Patterns to Look For

### Architecture Analysis
1. **Data Layer**: How is data accessed and managed?
2. **Business Logic**: Where are the core business rules implemented?
3. **Presentation Layer**: How is the UI structured and organized?
4. **Integration Points**: How does the system connect to external services?
5. **Cross-Cutting Concerns**: How are logging, error handling, and security managed?

### Performance Considerations
- **Identify bottlenecks** - Database queries, API calls, build processes
- **Understand caching strategies** - What's cached and where
- **Check bundle sizes** - For web applications, understand asset optimization
- **Review monitoring** - How is performance tracked and measured

### Team Dynamics
- **Code review process** - How does the team collaborate on code changes?
- **Testing culture** - What level of testing is expected?
- **Deployment confidence** - How comfortable is the team with changes?
- **Learning orientation** - Does the team prioritize learning or delivery?

## Red Flags to Avoid

### Technical Red Flags
- Creating abstractions without understanding existing patterns
- Ignoring performance characteristics when suggesting solutions
- Over-engineering solutions for simple problems
- Breaking existing APIs or interfaces without discussion

### Communication Red Flags
- Making assumptions about developer skill levels
- Providing solutions without explaining trade-offs
- Ignoring established team preferences
- Being too verbose or too terse for the audience

### Process Red Flags
- Suggesting changes to no-go areas
- Ignoring testing or deployment requirements
- Not considering backward compatibility
- Rushing to implement without proper analysis

## Success Patterns

### Effective Collaboration
- **Listen first** - Understand the problem before proposing solutions
- **Ask good questions** - Help clarify requirements and constraints
- **Provide options** - Give teams choices with clear trade-offs
- **Iterate together** - Build solutions collaboratively

### Quality Solutions
- **Solve the right problem** - Address root causes, not just symptoms
- **Consider maintainability** - Think about long-term code health
- **Respect constraints** - Work within established boundaries
- **Test thoroughly** - Ensure solutions work as expected

### Knowledge Transfer
- **Document decisions** - Help teams understand why solutions work
- **Share patterns** - Help teams recognize reusable approaches
- **Teach through examples** - Show good practices in action
- **Build team capabilities** - Help developers grow their skills

## Troubleshooting Common Issues

### "The AI doesn't understand our codebase"
- Check if project-context.md is up to date
- Verify that key patterns and entry points are documented
- Consider adding more architectural details or examples

### "The AI's suggestions don't fit our team"
- Review developer profiles for accuracy
- Update team preferences in project context
- Provide more specific feedback about what works/doesn't work

### "The AI makes changes that are too complex/simple"
- Calibrate based on developer experience levels
- Be explicit about preferred change sizes
- Provide examples of good vs overwhelming changes

## Customization Notes

Teams should customize this guide based on:
- **Technology stack specifics** - Add framework-specific guidance
- **Team culture** - Reflect actual working styles and preferences
- **Project constraints** - Include domain-specific considerations
- **Common issues** - Add patterns for recurring problems
