# Testing Guide for SCM Config Clone

## Test Setup Overview

We've established a comprehensive testing framework for the SCM Config Clone tool, focused on both unit and integration tests. The test structure is organized as follows:

```
tests/
├── conftest.py             # Shared pytest fixtures
├── README.md               # Testing documentation
├── factories/              # Factory Boy factories for test objects
│   ├── __init__.py
│   ├── mock_client.py      # Mock SCM client
│   └── model_factories.py  # Factories for model objects
├── integration/            # Integration tests
│   ├── __init__.py
│   └── test_command_workflows.py  # End-to-end workflow tests
└── unit/                   # Unit tests
    ├── __init__.py
    ├── test_main.py        # Tests for the main CLI application
    ├── test_network_commands.py  # Tests for network commands
    ├── test_settings.py    # Tests for settings module
    └── test_utilities_direct.py  # Tests for utility functions
```

## Running Tests

We've provided a test runner script (`run_tests.sh`) that simplifies running different test categories:

```bash
# Run all tests
./run_tests.sh

# Run only unit tests
./run_tests.sh unit

# Run only integration tests
./run_tests.sh integration

# Run only utility tests
./run_tests.sh utils

# Run only settings tests
./run_tests.sh settings
```

## Test Approaches

### Direct Testing

For utility modules that are standalone with minimal dependencies, we've used a direct testing approach in `test_utilities_direct.py`. This avoids dependencies on the SCM SDK and its import structure.

### Mock Objects with Factory Boy

For testing with SCM models, we've created Factory Boy factories that generate test objects. For example:

```python
from tests.factories.model_factories import AddressResponseModelFactory

# Create a test address object
address = AddressResponseModelFactory(name="test-address", ip_netmask="192.168.1.0/24")
```

### Mock SCM Client

We've implemented a mock SCM client that doesn't make real API calls, allowing us to test command behavior in isolation:

```python
from tests.factories.mock_client import MockScmApiFactory

# Create mock objects
source_objects = [AddressResponseModelFactory(), AddressResponseModelFactory()]

# Create a mock API with predefined response objects
mock_api = MockScmApiFactory.create_mock_api(
    api_class="Address",
    response_objects=source_objects
)
```

## Testing Challenges

During implementation, we encountered the following challenges:

1. **Import Dependencies**: The SCM client has dependencies that are difficult to mock completely. We adopted a hybrid approach with direct function testing for utilities.

2. **Coverage Reporting**: Due to the import structure and direct testing approach, coverage reporting does not currently function as expected. This is an area for future improvement.

3. **Circular Dependencies**: Some modules have circular dependencies, requiring special handling in tests.

## Next Steps for Testing

To further improve test coverage, consider:

1. Add mock tests for CLI commands that don't try to import the actual commands
2. Add more integration tests for common workflows
3. Add fixtures to generate standard test objects
4. Improve the test documentation

## Writing New Tests

When adding tests:

1. **Unit Tests**: Add to `tests/unit/` with appropriate names (`test_*.py`)
2. **Integration Tests**: Add to `tests/integration/` for workflow testing
3. **Fixtures**: Add common fixtures to `conftest.py`
4. **Factories**: Add new model factories to `factories/model_factories.py`

Remember to update the test runner script if you add new test categories.

## Running Individual Tests

To run a specific test file or test function:

```bash
# Run a specific test file
poetry run pytest tests/unit/test_utilities_direct.py

# Run a specific test
poetry run pytest tests/unit/test_utilities_direct.py::TestParseCSV::test_parse_csv_option_with_values
```