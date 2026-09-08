---
name: gtest-execute
description: Guide for running and filtering Google Tests, achieving 100% CTC coverage, and documenting test cases. Use this when asked to run tests, filter tests, achieve code coverage, or write test documentation.
---

# Google Test Execution and Coverage Guide

## Test Case Creation Guidelines

### Test Design Principles

#### 1. Code Coverage Requirements
- **CTC Coverage**: Condition/Decision Coverage must be 100%
  - Every condition in a decision must evaluate to both true and false
  - Every decision must take all possible outcomes
  - Test all branches in if/else, switch, loops, and logical operators

#### 2. Input Testing Strategy
- **Valid Input Tests**: Test all valid input combinations
  - Normal/expected values
  - Edge values within valid range
  - Typical use cases
  
- **Invalid Input Tests**: Test all invalid input scenarios
  - Out-of-range values
  - Null/empty inputs
  - Wrong data types
  - Malformed data
  - Negative values where positive expected
  - Unexpected state combinations

#### 3. Boundary Testing
Always test boundary conditions:
- **Lower boundary**: Minimum valid value
- **Lower boundary - 1**: Just below minimum (invalid)
- **Upper boundary**: Maximum valid value
- **Upper boundary + 1**: Just above maximum (invalid)
- **Zero**: For numeric inputs
- **Empty**: For strings/collections
- **Null/nullptr**: For pointers
- **First element**: For arrays/lists
- **Last element**: For arrays/lists

### Test Case Documentation Standard

Every test case MUST include a documentation block with:

```cpp
/**
 * Test Name: <DescriptiveCamelCaseName>
 * Input Parameters: 
 *   - param1: <type and description>
 *   - param2: <type and description>
 * Test Steps:
 *   1. <First action/setup step>
 *   2. <Second action>
 *   3. <Final action>
 * Expected Results:
 *   - <First expected outcome>
 *   - <Second expected outcome>
 */
TEST_F(TestFixture, TestName) {
    // Test implementation
}
```

### Documentation Template Examples

#### Example 1: Basic Function Test
```cpp
/**
 * Test Name: AddPositiveNumbers
 * Input Parameters:
 *   - a: int = 5
 *   - b: int = 3
 * Test Steps:
 *   1. Call add(5, 3)
 *   2. Verify return value
 * Expected Results:
 *   - Returns 8
 */
TEST(MathTest, AddPositiveNumbers) {
    EXPECT_EQ(add(5, 3), 8);
}
```

#### Example 2: Boundary Test
```cpp
/**
 * Test Name: SetValueAtUpperBoundary
 * Input Parameters:
 *   - value: int = 100 (maximum allowed)
 * Test Steps:
 *   1. Initialize object
 *   2. Call setValue(100)
 *   3. Verify value is accepted
 * Expected Results:
 *   - setValue() returns true
 *   - getValue() returns 100
 */
TEST_F(ObjectTest, SetValueAtUpperBoundary) {
    Object obj;
    EXPECT_TRUE(obj.setValue(100));
    EXPECT_EQ(obj.getValue(), 100);
}
```

#### Example 3: Invalid Input Test
```cpp
/**
 * Test Name: RejectsNegativeInput
 * Input Parameters:
 *   - value: int = -1 (invalid, must be >= 0)
 * Test Steps:
 *   1. Initialize object
 *   2. Attempt to set negative value
 *   3. Verify rejection
 * Expected Results:
 *   - setValue() returns false
 *   - getValue() remains at default (0)
 *   - Error flag is set
 */
TEST_F(ObjectTest, RejectsNegativeInput) {
    Object obj;
    EXPECT_FALSE(obj.setValue(-1));
    EXPECT_EQ(obj.getValue(), 0);
    EXPECT_TRUE(obj.hasError());
}
```

#### Example 4: State Transition Test
```cpp
/**
 * Test Name: IdleToRunningTransition
 * Input Parameters:
 *   - event: EVENT_START
 * Test Steps:
 *   1. Verify initial state is IDLE
 *   2. Send START event
 *   3. Check state changed to RUNNING
 *   4. Verify counter reset to 0
 * Expected Results:
 *   - State transitions from IDLE to RUNNING
 *   - Counter is reset to 0
 *   - No error flag set
 */
TEST_F(StateMachineTest, IdleToRunningTransition) {
    ASSERT_EQ(sm.state, STATE_IDLE);
    sm.processEvent(EVENT_START);
    EXPECT_EQ(sm.state, STATE_RUNNING);
    EXPECT_EQ(sm.counter, 0);
    EXPECT_FALSE(sm.hasError());
}
```

### Comprehensive Test Coverage Checklist

For each function/module, ensure tests cover:

- [ ] **Happy path**: Normal operation with valid inputs
- [ ] **All branches**: Every if/else, switch case, loop path
- [ ] **Boundary values**: Min, max, zero, empty
- [ ] **Invalid inputs**: Out of range, null, wrong type
- [ ] **Error conditions**: Exceptions, error codes, failures
- [ ] **State transitions**: All valid and invalid transitions
- [ ] **Edge cases**: Overflow, underflow, concurrent access
- [ ] **Combinations**: Multiple conditions together
- [ ] **Sequence**: Order of operations matters
- [ ] **Cleanup**: Resource deallocation, reset operations

### Test Naming Conventions

Use descriptive names that indicate what is being tested:
- `FunctionName_Condition_ExpectedBehavior`
- Examples:
  - `Divide_ByZero_ThrowsException`
  - `Connect_InvalidHost_ReturnsFalse`
  - `ProcessData_EmptyInput_ReturnsEmptyResult`
  - `StateIdle_OnStart_TransitionsToRunning`

## Running Google Tests

### Basic Execution
```bash
# Run all tests
./test_executable

# Windows
test_executable.exe
```

### Filtering Tests

#### Run specific test suite
```bash
./test_executable --gtest_filter=TestSuiteName.*
```

#### Run specific test
```bash
./test_executable --gtest_filter=TestSuiteName.TestName
```

#### Run multiple patterns
```bash
./test_executable --gtest_filter=Suite1.*:Suite2.Test*
```

#### Exclude tests
```bash
./test_executable --gtest_filter=-*Slow*
```

### Output Control

#### Verbose output
```bash
./test_executable --gtest_print_time=1
```

#### List all tests
```bash
./test_executable --gtest_list_tests
```

#### Run with detailed output
```bash
./test_executable --gtest_print_utf8=0
```

### Repeat and Shuffle

#### Repeat tests
```bash
./test_executable --gtest_repeat=10
```

#### Shuffle test order
```bash
./test_executable --gtest_shuffle
```

### Using CTest

```bash
# Run all tests
ctest

# Verbose output
ctest -V

# Show only failures
ctest --output-on-failure

# Run specific test
ctest -R TestName

# Exclude tests
ctest -E TestPattern

# Run tests in parallel
ctest -j4
```

### Best Practices

1. **Run tests frequently** during development
2. **Fix failures immediately** - don't let them accumulate
3. **Use filters** to focus on specific areas
4. **Check coverage** regularly to ensure 100% CTC
5. **Document failures** with clear reproduction steps
6. **Automate** test execution in CI/CD pipeline
