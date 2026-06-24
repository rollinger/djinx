from django.urls import path
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import Template, RequestContext

from .parser import SectionParser


class DxActionRouter:
    """Unify the Main User Loop into one class with many routed actions.
    Main User Loop = Request->Route->Logic->Render->Response ...

    1) define the dx_section_template
    2) set up actions as class methods with the route decorator
    3) hook the router into a url conf
    """

    # TODO: Alternative template_name.html
    dx_section_template = None

    def __init__(self, **kwargs):
        """Constructor builds the dx section cache."""
        if self.dx_section_template is None:
            raise ImproperlyConfigured("Must set a djxi section template")
        self.build_section_cache()

    def build_section_cache(self) -> None:
        """On init builds the section cache. A dictionary with the (k,v) = name, html_string."""
        self._dx_section_dict = self.parse_section_dict()

    def parse_section_dict(self) -> dict:
        """Parses the string and extract the dx-section parts."""
        parser = SectionParser()
        parser.feed(self.dx_section_template)
        return parser.sections

    def render_section(self, request, section_name, context=None):
        """Render a dx-section as a full HTTP response."""
        if context is None:
            context = {}
        raw_html = self.get_template_section(section_name)
        template = Template(raw_html)
        return HttpResponse(template.render(RequestContext(request, context)))

    def get_template_section(self, name: str) -> str:
        """Returns the dx-section template string for this view.
        If name cannot be found, returns empty string.
        """
        return self._dx_section_dict.get(name, "")

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
