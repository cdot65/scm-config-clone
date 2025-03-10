# SCM Config Clone Test Suite

This directory contains the test suite for the SCM Config Clone tool. The tests are organized into unit tests and integration tests.

## Test Structure

- `tests/unit/`: Unit tests for individual components
- `tests/integration/`: Integration tests for complete workflows
- `tests/factories/`: Factory Boy factories for creating test objects

## Running Tests

You can use the `run_tests.sh` script to run the tests:

```bash
# Run all tests
./run_tests.sh

# Run only unit tests
./run_tests.sh unit

# Run only integration tests
./run_tests.sh integration

# Run unit tests quickly without coverage
./run_tests.sh fast
```

Or you can use pytest directly:

```bash
# Run all tests with coverage
poetry run pytest --cov=scm_config_clone

# Run only unit tests
poetry run pytest tests/unit

# Run only a specific test file
poetry run pytest tests/unit/test_utilities.py

# Run a specific test
poetry run pytest tests/unit/test_utilities.py::TestParseCSV::test_parse_csv_option_with_values
```

## Coverage Reports

The test runner generates coverage reports in both terminal and HTML formats. The HTML report can be found at `htmlcov/index.html` after running the tests with coverage.

## Mock Objects

We use Factory Boy to create mock objects for testing. The factories are defined in `tests/factories/` and provide a consistent way to create test objects.

### Example: Creating mock objects

```python
from tests.factories.model_factories import AddressResponseModelFactory

# Create a basic address object
address = AddressResponseModelFactory()

# Create an address with specific attributes
custom_address = AddressResponseModelFactory(
    name="test-address",
    ip_netmask="192.168.1.0/24",
    description="Test address"
)
```

## Mock SCM Client

For testing the SCM API, we use a mock client that doesn't make real API calls. This client is defined in `tests/factories/mock_client.py`.

### Example: Using the mock SCM client

```python
from tests.factories.mock_client import MockScmApiFactory

# Create mock objects
source_objects = [AddressResponseModelFactory(), AddressResponseModelFactory()]

# Create a mock API with predefined response objects
mock_api = MockScmApiFactory.create_mock_api(
    api_class="Address",  # The API class being mocked
    response_objects=source_objects  # Objects to return from list() calls
)

# Now you can use the mock API in your tests
result = mock_api.list(folder="test-folder")
assert len(result) == 2
```

## Writing New Tests

When writing new tests:

1. Create unit tests for individual components
2. Create integration tests for complete workflows
3. Use Factory Boy factories to create test objects
4. Use descriptive test names following the convention `test_<function_name>_<scenario>`
5. Use pytest fixtures for common setup
6. Mock external dependencies to avoid network calls

### Example: Basic unit test structure

```python
def test_function_scenario():
    """Test that function behaves correctly in a specific scenario."""
    # Arrange (setup test data)
    input_data = "test"
    
    # Act (call the function)
    result = function_under_test(input_data)
    
    # Assert (check the results)
    assert result == expected_result
```

## Continuous Integration

The tests are run automatically in the CI/CD pipeline. The configuration is available in the GitHub Actions workflow files.