# pytest tests/test_config.py -v
from src.config import Config

def test_singleton_pattern():
    # Create two instances
    config1 = Config()
    config2 = Config()
    
    # Test that they are the same instance
    assert config1 is config2
    
    # Test that modifying one affects the other
    config1.TEST_VALUE = "test"
    assert hasattr(config2, "TEST_VALUE")
    assert config2.TEST_VALUE == "test"

def test_config_values():
    config = Config()
    
    # Test get method with existing attribute
    assert config.get('ENVIRONMENT') == config.ENVIRONMENT
    
    # Test get method with default value
    assert config.get('NON_EXISTENT', 'default') == 'default'