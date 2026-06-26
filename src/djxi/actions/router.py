""" Djxi Routing

TODO: Potential Refactor
- dx_route -> make_route | dx_view
- dx_router -> dx_collect_views
"""
from functools import wraps
from django.http import HttpResponseNotAllowed
from django.urls import path


class DXRouterMixin:
    """Use as a Mixin to call CLS.dx_router() to get a list of djxi routes"""

    @classmethod
    def dx_router(cls) -> list:
        """
        Generate a list of Django URL patterns from all methods decorated with @route.
        Use the class method to DxActionRouter.dx_router() in the url conf to hook the routes
        """
        patterns = []

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, "_routes"):
                for url_path, methods, name in attr._routes:
                    # Create a view that instantiates the class and calls the method
                    def make_view(method_name, allowed_methods, attr_func=attr):
                        @wraps(attr_func)
                        def view(request, *args, **kwargs):
                            if request.method not in allowed_methods:
                                return HttpResponseNotAllowed(allowed_methods)
                            instance = cls()  # instantiate the view class
                            handler = getattr(instance, method_name)
                            return handler(request, *args, **kwargs)

                        return view

                    patterns.append(
                        path(url_path, make_view(attr_name, methods), name=name)
                    )

        return patterns


def dx_route(path: str, methods: [] = None, **kwargs):
    """
    Decorator to mark a class method as a URL endpoint.
    - path: URL path (can include Django path converters, e.g. '/items/<int:id>/')
    - methods: list of allowed HTTP methods (defaults to ["GET"])
    - kwargs:
        - name: qualify the route with a name
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
