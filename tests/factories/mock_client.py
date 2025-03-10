"""
Mocks for SCM API client and related objects.
"""

import factory
from unittest.mock import MagicMock, patch
import pytest


class MockScmClient:
    """
    Mock SCM client for testing that doesn't make real API calls.
    """
    def __init__(self, client_id=None, client_secret=None, tsg_id=None, log_level=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tsg_id = tsg_id
        self.log_level = log_level
        
        # For tracking API calls
        self.calls = []


class MockScmApiFactory:
    """
    Factory for creating mock SCM API objects (Address, Tag, etc.)
    """
    @staticmethod
    def create_mock_api(api_class, response_objects=None, errors=None):
        """
        Create a mock SCM API object with predefined responses.
        
        Args:
            api_class: The API class being mocked (e.g., Address, Tag)
            response_objects: Optional list of objects to return from list() calls
            errors: Optional dict mapping method names to exceptions to raise
        
        Returns:
            A MagicMock configured with the specified behavior
        """
        mock_api = MagicMock()
        
        # Configure the list method to return provided objects or empty list
        mock_api.list.return_value = response_objects if response_objects else []
        
        # Configure the create method to return the first object or a mock
        if response_objects:
            mock_api.create.return_value = response_objects[0]
        
        # Configure error behavior if specified
        if errors:
            for method_name, exception in errors.items():
                getattr(mock_api, method_name).side_effect = exception
        
        return mock_api


@pytest.fixture
def mock_scm_client():
    """Fixture to provide a mock SCM client."""
    with patch('scm.client.Scm', MockScmClient):
        yield MockScmClient


@pytest.fixture
def mock_scm_api_factory():
    """Fixture to provide the mock API factory."""
    return MockScmApiFactory