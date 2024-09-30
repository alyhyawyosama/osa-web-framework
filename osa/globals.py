import contextvars # Import the contextvars module
from .local_proxy import LocalProxy
#Thanks to contextvars keeping track of separate contexts per request. This solves the issue of shared global state across threads or asynchronous coroutines.
#The contextvars module provides a way to store and retrieve values that are local to the current context, such as a task or request.

_app_ctx_var = contextvars.ContextVar('app', default=None)
_request_ctx_var = contextvars.ContextVar('request', default=None)
_response_ctx_var = contextvars.ContextVar('response', default=None)

current_app = LocalProxy(_app_ctx_var)
_no_req_msg = """\
Working outside of request context.
This typically means that you attempted to use functionality that needed
an active HTTP request. 
"""
# Create local proxies for request and response
request = LocalProxy(_request_ctx_var , _no_req_msg) 

_no_res_msg = """\
Working outside of response context.
This typically means that you attempted to use functionality that needed
an active HTTP response. 
"""

response = LocalProxy(_response_ctx_var,_no_res_msg )

