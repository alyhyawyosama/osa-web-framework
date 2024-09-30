import pytest
from webob import Request, Response
from osa.globals import _request_ctx_var, _response_ctx_var, request, response
import threading
def test_request_context():
    environ = {
        'PATH_INFO': '/test',
        'REQUEST_METHOD': 'GET',
        'wsgi.url_scheme': 'http',
    }
    req = Request(environ)
    _request_ctx_var.set(req)

    assert request.path == "/test"
    assert request.method == "GET"

def test_response_context():
    resp = Response()
    _response_ctx_var.set(resp)

    response.text = "Hello"
    assert response.text == "Hello"
