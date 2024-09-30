# import contextvars


# import contextvars

class LocalProxy:
    def __init__(self, context_var, unbound_message=None):
        self._context_var = context_var
        self._unbound_message = unbound_message

    def _get_current_object(self):
        obj = self._context_var.get(None)
        if obj is None:
            raise RuntimeError(self._unbound_message)
        return obj

    def __getattr__(self, name):
        current_object = self._get_current_object()
        return getattr(current_object, name)

    def __setattr__(self, name, value):
        if name in ("_context_var", "_unbound_message"):
            super().__setattr__(name, value)
        else:
            current_object = self._get_current_object()
            setattr(current_object, name, value)

# # Create context variables for request and response

