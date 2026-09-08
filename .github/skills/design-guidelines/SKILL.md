---
name: design-guidelines
description: System architecture and design guidelines for software development. Use this when asked about architecture, design patterns, module structure, or best practices for software design.
---

# System Design Guidelines

## Architecture Principles

### Modularity
- Design systems with clear module boundaries
- Each module should have a single, well-defined responsibility
- Minimize dependencies between modules
- Use interfaces to decouple implementations

### Testability
- Design for testability from the start
- Use dependency injection to allow mock substitution
- Avoid tight coupling between components
- Make state observable and controllable

### Maintainability
- Write self-documenting code
- Follow consistent naming conventions
- Keep functions small and focused
- Document design decisions and rationale

## Design Patterns

### Common Patterns to Use

#### 1. Dependency Injection
Inject dependencies rather than creating them internally:
```cpp
// Good: Dependencies injected
class Service {
public:
    explicit Service(Database* db) : db_(db) {}
private:
    Database* db_;
};

// Bad: Creates dependency internally
class Service {
public:
    Service() : db_(new ConcreteDatabase()) {}
private:
    Database* db_;
};
```

#### 2. Interface Segregation
Use focused interfaces rather than large monolithic ones:
```cpp
// Good: Focused interfaces
class Readable {
public:
    virtual ~Readable() = default;
    virtual std::string read() = 0;
};

class Writable {
public:
    virtual ~Writable() = default;
    virtual void write(const std::string& data) = 0;
};

// Bad: Fat interface
class ReadWrite {
public:
    virtual std::string read() = 0;
    virtual void write(const std::string& data) = 0;
    virtual void flush() = 0;
    virtual void close() = 0;
};
```

#### 3. Factory Pattern
Use factories for complex object creation:
```cpp
class ConnectionFactory {
public:
    static std::unique_ptr<Connection> create(const Config& config) {
        if (config.type == "http") {
            return std::make_unique<HttpConnection>(config);
        } else if (config.type == "websocket") {
            return std::make_unique<WebSocketConnection>(config);
        }
        return nullptr;
    }
};
```

## Module Structure

### Recommended Organization

```
project/
├── include/          # Public headers
│   └── module/
│       ├── interface.h
│       └── types.h
├── src/             # Implementation files
│   └── module/
│       ├── implementation.cpp
│       └── internal.h
└── test/            # Unit tests
    └── module/
        ├── test_implementation.cpp
        └── mock_interface.h
```

### Header Guidelines

1. **Use header guards or `#pragma once`**
2. **Minimize includes in headers** - prefer forward declarations
3. **Separate interface from implementation** - keep headers clean
4. **Document public APIs** - explain purpose and usage

## Best Practices

### Code Organization

1. **Single Responsibility**: Each class/function does one thing well
2. **DRY (Don't Repeat Yourself)**: Extract common logic into reusable functions
3. **YAGNI (You Aren't Gonna Need It)**: Don't add functionality until needed
4. **KISS (Keep It Simple, Stupid)**: Prefer simple solutions

### Error Handling

1. **Use exceptions for exceptional cases**, not control flow
2. **Document error conditions** in function documentation
3. **Validate inputs** early and fail fast
4. **Provide meaningful error messages**

### Performance Considerations

1. **Measure before optimizing** - don't guess
2. **Optimize algorithms** before micro-optimizations
3. **Consider memory allocation patterns**
4. **Use appropriate data structures** for the access pattern

### Documentation

1. **Document interfaces and public APIs**
2. **Explain "why" not "what"** - code shows what, comments explain why
3. **Keep documentation close to code**
4. **Update documentation with code changes**

## Design Review Checklist

Before finalizing a design, verify:

- [ ] **Clear responsibilities**: Each component has a well-defined purpose
- [ ] **Testable**: Can be unit tested with mocks
- [ ] **Maintainable**: Code is readable and understandable
- [ ] **Loosely coupled**: Minimal dependencies between modules
- [ ] **Extensible**: Can add features without major refactoring
- [ ] **Error handling**: All error cases are handled
- [ ] **Performance**: Meets performance requirements
- [ ] **Documentation**: Key decisions and APIs are documented
