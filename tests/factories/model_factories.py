"""
Factory Boy factories for SCM object models.
"""

import factory
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class BaseModelFactory(factory.Factory):
    """Base factory for SCM model objects."""
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance using model_class constructor."""
        # This simulates the behavior of Pydantic models
        return model_class(**kwargs)


class FakeAddress:
    """Fake address model for testing."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        # Set default values for required fields if not provided
        if 'id' not in kwargs:
            self.id = factory.Faker('uuid4').generate({})
        if 'name' not in kwargs:
            self.name = factory.Faker('word').generate({})


class AddressResponseModelFactory(BaseModelFactory):
    """Factory for AddressResponseModel objects."""
    
    class Meta:
        model = FakeAddress
    
    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence', nb_words=5)
    folder = "test-folder"
    snippet = None
    device = None
    tag = factory.LazyFunction(lambda: [])
    ip_netmask = factory.LazyAttribute(lambda o: "192.168.1.0/24" if not any([o.fqdn, o.ip_range, o.ip_wildcard]) else None)
    fqdn = None
    ip_range = None
    ip_wildcard = None
    created_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    modified_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())


class FakeTag:
    """Fake tag model for testing."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        # Set default values for required fields if not provided
        if 'id' not in kwargs:
            self.id = factory.Faker('uuid4').generate({})
        if 'name' not in kwargs:
            self.name = factory.Faker('word').generate({})


class TagResponseModelFactory(BaseModelFactory):
    """Factory for TagResponseModel objects."""
    
    class Meta:
        model = FakeTag
    
    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    color = factory.LazyFunction(lambda: "color{}".format(factory.random.randint(1, 16)))
    comments = factory.Faker('sentence')
    folder = "test-folder"
    snippet = None
    device = None
    created_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    modified_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())


class FakeService:
    """Fake service model for testing."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
        # Set default values for required fields if not provided
        if 'id' not in kwargs:
            self.id = factory.Faker('uuid4').generate({})
        if 'name' not in kwargs:
            self.name = factory.Faker('word').generate({})


class ServiceResponseModelFactory(BaseModelFactory):
    """Factory for ServiceResponseModel objects."""
    
    class Meta:
        model = FakeService
    
    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('sentence')
    protocol = factory.LazyFunction(lambda: "tcp")
    port = factory.LazyFunction(lambda: "443")
    source_port = None
    tag = factory.LazyFunction(lambda: [])
    folder = "test-folder"
    snippet = None
    device = None
    created_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())
    modified_on = factory.LazyFunction(lambda: datetime.now(timezone.utc).isoformat())