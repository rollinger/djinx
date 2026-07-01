""" Djxi Routing """
from functools import wraps
from django.http import HttpResponseNotAllowed
from django.urls import path

DX_SUPPORTED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


class DXRouterMixin:
    """Provides a interface for extracting urls from methods wrapped with dx_action.
    Use as a Mixin to call CLS.url_patterns() to get a list of djxi routes
    """

    @classmethod
    def url_patterns(cls) -> list:
        """
        Generate a list of Django URL patterns from all methods decorated with @route.
        Use the class method to DXEndpointBattery.url_patterns() in the url conf to hook the routes
        """
        patterns = []

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, "_dx_routes"):
                for url_path, methods, name in attr._dx_routes:
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


def dx_action(path: str, methods: [] = None, **kwargs):
    """
    Decorator to mark a class method as a URL endpoint.
    - path: URL path (can include Django path converters, e.g. '/items/<int:id>/')
    - methods: list of allowed HTTP methods (defaults to ["GET"])
    - kwargs:
        - name: qualify the route with a name, default to func.__name__
    """
    if methods is None:
        methods = ["GET"]
    methods = [m.upper() for m in methods]
    # Return a noop decorator if any method is not in the SUPPORTED METHODS
    if not all(m in DX_SUPPORTED_METHODS for m in methods):

        def decorator_noop(func):
            return func

        return decorator_noop

    def decorator(func):
        name = kwargs.pop("name", func.__name__)
        if not hasattr(func, "_dx_routes"):
            func._dx_routes = []
        func._dx_routes.append((path, methods, name))
        return func

    return decorator


#
# Alias definitions (Shortcuts)
#
def dx_get(path: str, **kwargs):
    return dx_action(path, ["GET"], **kwargs)


def dx_post(path: str, **kwargs):
    return dx_action(path, ["POST"], **kwargs)


def dx_put(path: str, **kwargs):
    return dx_action(path, ["PUT"], **kwargs)


def dx_patch(path: str, **kwargs):
    return dx_action(path, ["PATCH"], **kwargs)


def dx_delete(path: str, **kwargs):
    return dx_action(path, ["DELETE"], **kwargs)
