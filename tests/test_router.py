import pytest
from osa.router import  Router
from osa.exceptions import  HTTPException

@pytest.fixture
def router():
    return Router()

def test_add_route(router):
    router.add_route('/test', 'handler', ['GET'])
    assert '/test' in router.routes

    with pytest.raises(AssertionError):
        router.add_route('/test', 'handler', ['GET'])

def test_router_match(router):
    router.add_route('/test/{param}', 'handler', ['GET'])
    matched_route, params = router.match('/test/value')
    assert matched_route is not None
    assert params['param'] == 'value'
    with pytest.raises(HTTPException):
        router.match('/no_match')

def test_get_handler( router):
    class Handler:
        def get(self):
            return 'GET response'

    router.add_route('/test', Handler, ['GET'])
    route = router.routes['/test']

    handler = router.get_handler(route, 'GET')
    assert handler() == 'GET response'
    with pytest.raises(HTTPException):
        router.get_handler(route, 'POST')
