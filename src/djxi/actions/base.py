from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template import Template, RequestContext

from .parser import SectionParser, load_django_template
from .router import DXRouterMixin


class DxActionRouter(DXRouterMixin):
    """Unify the Main User Loop into one class with defined routed actions and a section library.
    Main User Loop = Request->Route->Logic->Render->Response ...

    1) define the section template:
        a) inline_template = <dx-section name="identifier"> html for this section </dx-section>
        b) template_name = path/to/template.html (app/template.html)
    2) set up actions as class methods with the route decorator
    3) hook the router into a url conf
    """

    inline_template = None
    template_name = None

    def __init__(self, **kwargs):
        """Constructor builds the dx section cache."""
        if self.inline_template is None and self.template_name is None:
            raise ImproperlyConfigured(
                "DxActionRouter requires a definition of "
                "'inline_template' or a path to a 'template_name'"
            )
        self.build_section_cache()

    def build_section_cache(self) -> None:
        """On init builds the section cache. A dictionary with the (k,v) = name, html_string."""
        self._dx_section_dict = self.parse_section_dict()

    def parse_section_dict(self) -> dict:
        """Parses the string and extract the dx-section parts."""
        parser = SectionParser()
        parser.feed(self.get_dx_template_string())
        return parser.sections

    def get_dx_template_string(self) -> str:
        """Concatenates the specified templates and returns the unmodified string.
        In most cases you want to set eighter or, yet both is allowed.
        """
        template_string = ""
        if self.template_name is not None:
            template_string = load_django_template(self.template_name)
        if self.inline_template is not None:
            template_string += self.inline_template
        return template_string

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
