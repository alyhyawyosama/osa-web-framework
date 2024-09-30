# app.py
from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from .template_engine import TemplateEngine
from .static_file_handler import StaticFileHandler
from .router import Router
from .error_handlers import debug_exception_handler 
from .globals import request , response 
from .ctx import RequestContext , ResponseContext


class Osa:
    def __init__(self, templates_dir="templates", static_dir="static",debug=True):
        self.router = Router()  
        # self.static_file_handler = StaticFileHandler(static_dir)
        self.static_handler = StaticFileHandler(static_dir)
        self.templates_env = TemplateEngine(templates_dir)  
        self.before_request_funcs = []
        self.after_request_funcs = []
        self.error_handlers = {}  
        self.debug = debug
        self._static_root = "/static" 
    
    def wsgi_app(self, environ, start_response):
        ctx = self.request_context(environ)
        try:
            ctx.push()
            response = self.dispatch_request()
            return response(environ, start_response)
        finally:
            ctx.pop()
            
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def request_context(self,environ):    
        return RequestContext(environ)
    
    def route(self, rule, methods=None):
        """
        Route decorator to add routes similar to Flask's `@app.route()`.
        """
        def decorator(f):
            self.router.add_route(rule, f, methods)
            return f
        return decorator
            
    def dispatch_request(self):
        """
        Dispatches the request to the appropriate handler (view function).
        """
        res_ctx = ResponseContext()
        try :
            try:
                if self.is_static_file():
                    static_path = self.cut_static_root()
                    return self.static_handler.serve(static_path, request)
                self.run_before_request()
                
                res_ctx.push()
                
                response = res_ctx.current 
                # Find and run the handler for the route
                route, kwargs = self.router.match(request.path)
                handler = self.router.get_handler(route, request.method)
                # Call the handler with the route parameters
                handler(**kwargs)                
                # Run after request hooks
                self.run_after_request()
            except Exception as e:
                self.handle_exception(e )
            return response
        finally :
            res_ctx.pop()
            
    def handle_exception(self, e):
        """
        Handles exceptions like 404, 500 errors .
        """
        status_code = getattr(e, 'status', 500)
        response.status = status_code
        handler = self.error_handlers.get(status_code)
        if handler:
            return handler()
        if not self.debug:
            response.text = str(e)
            return response 
        debug_exception_handler(response,e)

    def template(self, template_name, context=None):
        return self.templates_env.render(template_name, context)
    
    def after_request(self,fun):
        """
        Register a function to run after each request.
        E.g. to modify response headers or log requests.
        @app.after_request
        def log_request():
            logger.info(f"{request.method} - {request.path}")
        """
        self.after_request_funcs.append(fun)
        return fun
    
    def before_request(self,fun):
        """
        Register a function to run before each request.
        E.g. to setup a database connection or authenticate a user.
        @app.before_request 
        def setup_request():
            request.db = get_database_connection()
        """
        self.before_request_funcs.append(fun)
        return fun
    
    def errorhandler(self, status_code):
        """
        Register custom error handlers, similar to Flask's `@app.errorhandler()`.
        """
        def decorator(func):
            self.error_handlers[status_code] = func
            return func
        return decorator
    
    def run_before_request(self):
        """
        Executes all registered `before_request` functions.
        """
        for func in self.before_request_funcs:
            func()

    def run_after_request(self):
        """
        Executes all registered `after_request` functions.
        """
        for func in reversed(self.after_request_funcs):
            func()
            
    def run(self, host="localhost", port=5000):
        from wsgiref.simple_server import make_server
        server = make_server(host, port, self)
        print(f"Starting server on http://{host}:{port}")
        server.serve_forever() 

    def test_session(self, base_url="http://testserver"):
        """
        Creates a test client to test the application.
        """
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session

    def is_static_file(self):
        return request.path.startswith(self._static_root)

    def cut_static_root(self):
        return request.path[len(self._static_root):]
         # /static/css/style.css -> /css/style.css




"""



""" 

 
 
 