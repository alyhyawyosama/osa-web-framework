# conftest.py
import pytest
import osa
from .utils import TEST_URL 
@pytest.fixture
def app():
    return osa.Osa(templates_dir="tests/templates", debug=False)


@pytest.fixture
def client(app):
    return app.test_session(base_url=TEST_URL)
