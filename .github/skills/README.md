# Agent Skills Quick Reference

## What Are Agent Skills?

Agent Skills are automatically loaded by GitHub Copilot when relevant to your question. They follow the [open Agent Skills standard](https://github.com/agentskills/agentskills).

## Available Skills

### 1. gtest-mock
**Location**: `.github/skills/gtest-mock/SKILL.md`

**Use when**: Creating mock objects, setting up EXPECT_CALL, testing with mocks

**Covers**:
- MOCK_METHOD syntax
- EXPECT_CALL patterns
- Matchers (_, StartsWith, HasSubstr)
- Cardinality (Times, AtLeast, AtMost)
- Return values and exceptions
- Best practices

### 2. gtest-execute
**Location**: `.github/skills/gtest-execute/SKILL.md`

**Use when**: Running tests, achieving code coverage, documenting test cases

**Covers**:
- Test execution and filtering
- 100% CTC coverage requirements
- Test documentation standards
- Boundary testing strategies
- Input validation testing
- CTest integration

### 3. design-guidelines
**Location**: `.github/skills/design-guidelines/SKILL.md`

**Use when**: Designing architecture, choosing patterns, structuring code

**Covers**:
- Design principles (SOLID, DRY, KISS)
- Common patterns (Dependency Injection, Factory)
- Module organization
- Error handling strategies
- Design review checklist

## How to Use

Simply ask Copilot your question - skills load automatically!

**Examples**:
```
"How do I mock a database class?"
→ Automatically loads gtest-mock skill

"How do I run only failed tests?"
→ Automatically loads gtest-execute skill

"What design pattern should I use for object creation?"
→ Automatically loads design-guidelines skill
```

## Adding New Skills

1. Create subdirectory in `.github/skills/`
2. Add `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: When to use this skill (include keywords)
---

# Skill Content
Your documentation here...
```

3. Commit - Copilot auto-discovers it!

## Learn More

- [GitHub Copilot Agent Skills Documentation](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [Agent Skills Standard](https://github.com/agentskills/agentskills)
