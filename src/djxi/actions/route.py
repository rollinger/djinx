def dx_route(path: str, methods=None):
    """
    Decorator to mark a class method as a URL endpoint.
    - path: URL path (can include Django path converters, e.g. '/items/<int:id>/')
    - methods: list of allowed HTTP methods (defaults to ["GET"])
    """
    if methods is None:
        methods = ["GET"]

    def decorator(func):
        if not hasattr(func, "_routes"):
            func._routes = []
        func._routes.append((path, methods))
        return func

    return decorator
