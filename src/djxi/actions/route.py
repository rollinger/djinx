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


#
# Alias definitions
#
def dx_GET(path: str, **kwargs):
    return dx_route(path, ["GET"], **kwargs)


def dx_HEAD(path: str, **kwargs):
    return dx_route(path, ["HEAD"], **kwargs)


def dx_POST(path: str, **kwargs):
    return dx_route(path, ["POST"], **kwargs)


def dx_PUT(path: str, **kwargs):
    return dx_route(path, ["PUT"], **kwargs)


def dx_PATCH(path: str, **kwargs):
    return dx_route(path, ["PATCH"], **kwargs)


def dx_DELETE(path: str, **kwargs):
    return dx_route(path, ["DELETE"], **kwargs)


def dx_OPTIONS(path: str, **kwargs):
    return dx_route(path, ["OPTIONS"], **kwargs)


def dx_ANY(path: str, **kwargs):
    return dx_route(
        path,
        ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        **kwargs,
    )
