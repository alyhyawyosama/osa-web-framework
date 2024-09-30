import pytest
from osa.globals import response
from .utils import abs_url
def test_basic_routes(app):
    @app.route("/home1")
    def home1():
        response.text = "YOLO"

    @app.route("/home2")
    def home2():
        response.text = "YOLO"

def test_duplicate_route_raises_exception(app):
    @app.route("/home2")
    def home2():
        response.text = "YOLO"

    # Test that the method will raise an exception error
    with pytest.raises(AssertionError):
        @app.route("/home2")
        def home2_duplicate():
            response.text = "YOLO"

def test_client_can_send_get_requests(app, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @app.route("/cool", methods=["GET"])
    def cool():
        response.text = RESPONSE_TEXT

    assert client.get(abs_url("/cool")).text == RESPONSE_TEXT

def test_parameterized_route(app, client):
    @app.route("/{name}")
    def greet(name):
        response.text = f"hey {name}"

    assert client.get(abs_url("/osama")).text == "hey osama"
    assert client.get(abs_url("/man")).text == "hey man"

def test_default_404_response(client):
    res = client.get(abs_url("/doesnotexist"))
    assert res.status_code == 404

def test_class_based_handler_get(app, client):
    RESPONSE_TEXT = "YOLO"

    @app.route("/home", methods=["GET"])
    class HomeHandler:
        def get(self):
            response.text = RESPONSE_TEXT

    assert client.get(abs_url("/home")).text == RESPONSE_TEXT

def test_class_based_handler_post(app, client):
    RESPONSE_TEXT = "YOLO"

    @app.route("/home", methods=["POST"])
    class HomeHandler:
        def post(self):
            response.text = RESPONSE_TEXT

    assert client.post(abs_url("/home")).text == RESPONSE_TEXT

def test_class_based_handler_method_not_allowed(app, client):
    @app.route("/test_class")
    class TestClassHandler:
        def post(self):
            response.text = "POST"

    res = client.get(abs_url("/test_class"))
    assert res.status_code == 405