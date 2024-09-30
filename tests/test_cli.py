
from osa.cli import  find_app_module , NoAppException


# test_osa.py
import os
import importlib.util
import pytest

@pytest.fixture(autouse=True)
def cleanup_env_vars():
    """Fixture to clean up environment variables after tests."""
    original_value = os.getenv('OSA_APP')
    yield
    if original_value is None:
        if 'OSA_APP' in os.environ:
            del os.environ['OSA_APP']
    else:
        os.environ['OSA_APP'] = original_value


def test_find_app_module_with_env_var(app):
    """Test finding app module via OSA_APP environment variable."""
    os.environ['OSA_APP'] = 'test_app'  # Name of the test app module
    # Create a dummy test_app.py in the current directory
    with open('test_app.py', 'w') as f:
        f.write('app = "This is a test app"')

    try:
        app_instance = find_app_module()
        assert app_instance == "This is a test app"
    finally:
        os.remove('test_app.py')  # Cleanup after test


# def test_find_app_module_with_default(app):
#     """Test finding app module by default app.py file."""
#     # Create a dummy app.py in the current directory
#     with open('wsgi.py', 'w') as f:
#         f.write('app = "This is the default app"')

#     try:
#         app_instance = find_app_module()
#         assert app_instance == "This is the default app"
#     finally:
#         os.remove('wsgi.py')  # Cleanup after test

def test_find_app_module_no_app_found():
    
    """Test when no app module is found """
    with pytest.raises(NoAppException):
        find_app_module("app:not_found")
