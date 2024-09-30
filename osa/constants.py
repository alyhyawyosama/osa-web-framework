
HTTPMethod = (
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'OPTIONS',
    'PATCH',
    'CONNECT',
    'TRACE'
)

empty_wsgi_application = lambda *args, **kwargs: None