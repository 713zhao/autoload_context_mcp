# GTest Mock
How to mock dependencies using gmock.

## Overview
Google Mock (gmock) is a framework for creating mock objects in C++ unit tests. It allows you to verify interactions with dependencies without requiring the actual implementation.

## Creating a Mock Class

### 1. Define the Interface
```cpp
// database.h
class Database {
public:
    virtual ~Database() = default;
    virtual void connect(const std::string& host) = 0;
    virtual bool query(const std::string& sql) = 0;
    virtual int getRecordCount() = 0;
};
```

### 2. Create the Mock
```cpp
// mock_database.h
#include <gmock/gmock.h>
#include "database.h"

class MockDatabase : public Database {
public:
    MOCK_METHOD(void, connect, (const std::string& host), (override));
    MOCK_METHOD(bool, query, (const std::string& sql), (override));
    MOCK_METHOD(int, getRecordCount, (), (override));
};
```

## Using Mocks in Tests

### Basic Expectations
```cpp
#include <gtest/gtest.h>
#include "mock_database.h"

TEST(ServiceTest, ConnectsToDatabase) {
    MockDatabase mock_db;
    
    // Expect connect to be called once with "localhost"
    EXPECT_CALL(mock_db, connect("localhost"))
        .Times(1);
    
    // Your code that should call connect
    Service service(&mock_db);
    service.initialize();
}
```

### Return Values
```cpp
TEST(ServiceTest, QueriesDatabase) {
    MockDatabase mock_db;
    
    // Specify return value
    EXPECT_CALL(mock_db, query("SELECT * FROM users"))
        .WillOnce(testing::Return(true));
    
    Service service(&mock_db);
    bool result = service.fetchUsers();
    
    EXPECT_TRUE(result);
}
```

### Multiple Calls
```cpp
TEST(ServiceTest, MultipleCalls) {
    MockDatabase mock_db;
    
    // Expect multiple calls with different arguments
    EXPECT_CALL(mock_db, query("SELECT * FROM users"))
        .Times(2)
        .WillRepeatedly(testing::Return(true));
    
    EXPECT_CALL(mock_db, getRecordCount())
        .WillOnce(testing::Return(10))
        .WillOnce(testing::Return(20));
}
```

## Common Matchers

### Argument Matching
```cpp
using ::testing::_;
using ::testing::StartsWith;
using ::testing::HasSubstr;

// Any argument
EXPECT_CALL(mock_db, connect(_));

// String matching
EXPECT_CALL(mock_db, query(StartsWith("SELECT")));
EXPECT_CALL(mock_db, query(HasSubstr("users")));
```

### Cardinality
```cpp
using ::testing::AtLeast;
using ::testing::AtMost;

EXPECT_CALL(mock_db, connect(_))
    .Times(AtLeast(1));

EXPECT_CALL(mock_db, query(_))
    .Times(AtMost(5));
```

## Best Practices

1. **Mock Interfaces, Not Implementations**: Always mock pure virtual interfaces
2. **Verify Behavior, Not Implementation**: Focus on what should happen, not how
3. **Use Appropriate Cardinality**: Be specific about expected call counts
4. **One Mock Per Test**: Keep tests isolated and focused
5. **Clean Up**: Use `testing::Mock::VerifyAndClearExpectations()` when needed

## Common Patterns

### Injecting Mocks
```cpp
class Service {
public:
    explicit Service(Database* db) : db_(db) {}
    
    void initialize() {
        db_->connect("localhost");
    }

private:
    Database* db_;
};
```

### Testing Error Conditions
```cpp
TEST(ServiceTest, HandlesConnectionFailure) {
    MockDatabase mock_db;
    
    EXPECT_CALL(mock_db, connect(_))
        .WillOnce(testing::Throw(std::runtime_error("Connection failed")));
    
    Service service(&mock_db);
    EXPECT_THROW(service.initialize(), std::runtime_error);
}
```
