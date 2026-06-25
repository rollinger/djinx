def dx_route(path: str, methods: [] = None, **kwargs):
    """
    Decorator to mark a class method as a URL endpoint.
    - path: URL path (can include Django path converters, e.g. '/items/<int:id>/')
    - methods: list of allowed HTTP methods (defaults to ["GET"])
    """
    if methods is None:
        methods = ["GET"]

    def decorator(func):
        name = kwargs.pop("name", func.__name__)
        if not hasattr(func, "_routes"):
            func._routes = []
        func._routes.append((path, methods, name))
        return func

    return decorator
