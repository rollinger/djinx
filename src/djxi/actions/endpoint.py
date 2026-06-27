from django.http import HttpResponse

from django.template import Template, RequestContext

from .messages import fetch_messages_template
from .router import DXRouterMixin
from .section import DXSectionMixin


class DXEndpointBattery(DXSectionMixin, DXRouterMixin):
    """Unify the Main User Loop into one class with defined routed actions and a section library.
    Main User Loop = Request->Route->Logic->Render->Response ...

    1) define the section template:
        a) inline_template = <dx-section name="identifier"> html for this section </dx-section>
        b) template_name = path/to/template.html (app/template.html)
    2) set up actions as class methods with the route decorator
    3) hook the router into a url conf
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render_section(self, request, section_name, context=None):
        """Render a dx-section as a full HTTP response."""
        if context is None:
            context = {}
        raw_html = self.get_section(section_name)
        msg_html = fetch_messages_template(request)
        template = Template(raw_html + msg_html)
        return HttpResponse(template.render(RequestContext(request, context)))
