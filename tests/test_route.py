
import pytest
from osa.router import Route


@pytest.fixture
def route():
    return Route('/test/{param}', 'handler', ['GET', 'POST'])

def test_route_match( route):
    print(route.methods)
    matched_route, params = route.match('/test/value')
    assert matched_route is not None
    assert params['param'] == 'value'

    matched_route, params = route.match('/no-match')
    assert matched_route is None
    assert params is None

def test_allows_method( route):
    assert route.allows_method('GET') is True
    assert route.allows_method('POST') is True
    assert route.allows_method('DELETE') is False
