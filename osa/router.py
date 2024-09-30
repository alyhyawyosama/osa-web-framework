from parse import parse
from osa.exceptions import abort
from osa.constants import HTTPMethod
import inspect

class Route:
    def __init__(self, rule, endpoint, methods=None):
        if methods is None:
            methods = [method for method in HTTPMethod]
        self.rule = rule
        self.endpoint = endpoint
        self.methods = [method.upper() for method in methods]

    def match(self, request_path):
        """
        Tries to match the request path to the route's rule.
        """
        rule = self.rule.replace('<', '{').replace('>', '}') # convert route rule to parse format .e.g /user/<id> to /user/{id}
        result = parse(rule, request_path)
        if result:
            return self, result.named
        return None, None

    def allows_method(self, method):
        """
        Checks if the request method is allowed for this route.
        """
        return method.upper() in self.methods


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, rule, handler, methods):
        assert rule not in self.routes, f"Route with rule {rule} already exists."
        
        """
        Adds a route to the router.
        """
        self.routes[rule] = Route(rule, handler, methods)

    def match(self, path):
        """
        Find the matching route for the request path.
        """
        for route in self.routes.values():
            matched_route, params = route.match(path)
            if matched_route:
                return matched_route, params
        abort(404)
        
    def get_handler(self, route, method):
        """
        Get the handler function if the method is allowed for the route.
        """
        if inspect.isclass(route.endpoint):
            handler_instance = route.endpoint()
            handler_function = getattr(handler_instance, method.lower(), None)
            # if the method is not implemented in the class, return 405
            if handler_function is None :
                abort(405)
            if not route.allows_method(method):
                abort(405)
            return handler_function
        else:
            if not route.allows_method(method):
                abort(405)
            return route.endpoint
