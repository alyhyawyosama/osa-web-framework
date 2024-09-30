from webob import Request, Response
from .globals import _request_ctx_var, _response_ctx_var

class RequestContext:
    """
    The request context contains per-request information. The Osa
    app creates and pushes it at the beginning of the request,
    then pops it at the end of the request.
    It will create the request object for the WSGI environment provided.
    """
    def __init__(self, environ):
        self.request = Request(environ)

    def push(self):
        """
        Push the request context to the context variable stack.
        """
        return _request_ctx_var.set(self.request)

    def pop(self):
        """
        Pop the current request context from the stack.
        """
        _request_ctx_var.set(None)

    @property
    def current(self):
        """
        Get the current request context.
        """
        return _request_ctx_var.get()



class ResponseContext:
    """
    Response context to handle per-request data like response. 
    """
    def __init__(self):
        self.response = Response()

    def push(self):
        """
        Push the response context to the context variable stack.
        """
        return _response_ctx_var.set(self.response)

    def pop(self):
        """
        Pop the current response context from the stack.
        """
        _response_ctx_var.set(None)

    @property
    def current(self):
        """
        Get the current response context.
        """
        return _response_ctx_var.get()

