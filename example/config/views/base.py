"""
Base Generic Class Views

inspired by Django's generic views.
See: https://ccbv.co.uk/projects/Django/5.2/django.views.generic.base/View/
"""
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseNotAllowed
from django.template import Template, RequestContext
from django.http import HttpResponse

from .parser import compile_section_dict
from django.urls import path


class DjinxEndpointMixin:
    # TODO: Alternative template_name.html
    dx_section_template = None

    def __init__(self, **kwargs):
        """Constructor builds the dx section template."""
        if self.dx_section_template is None:
            raise ImproperlyConfigured("Must set a dx-section template")
        self.build_dx_sections()

    def build_dx_sections(self) -> None:
        """Called on class initialization."""
        self._dx_section_dict = compile_section_dict(self.dx_section_template)

    def get_template_section(self, name: str) -> str:
        """Returns the dx-section template for this view.
        If name cannot be found, returns empty string.
        """
        return self._dx_section_dict.get(name, "")

    def render_section(self, request, section_name, context=None):
        """Render a dx-section as a full HTTP response."""
        if context is None:
            context = {}
        raw_html = self.get_template_section(section_name)
        template = Template(raw_html)
        return HttpResponse(template.render(RequestContext(request, context)))

    @classmethod
    def router(cls):
        """
        Generate a list of Django URL patterns from all methods
        decorated with @route.
        """
        patterns = []

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if hasattr(attr, "_routes"):
                for url_path, methods in attr._routes:
                    # Create a view that instantiates the class and calls the method
                    def make_view(method_name, allowed_methods):
                        def view(request, *args, **kwargs):
                            if request.method not in allowed_methods:
                                return HttpResponseNotAllowed(allowed_methods)
                            instance = cls()  # instantiate the view class
                            handler = getattr(instance, method_name)
                            return handler(request, *args, **kwargs)

                        return view

                    patterns.append(path(url_path, make_view(attr_name, methods)))

        return patterns
