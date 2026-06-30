from django.contrib import messages
from djxi.endpoint import DXEndpointBattery
from djxi.router import dx_route

TEMPLATE = """
<dx-section name="agreement">
    <div>Read this before confirm</div>
    <div hx-get='{% url "showcase:load-check-button" %}' hx-trigger="revealed delay:1s" hx-swap="outerHTML">Loading...</div>
</dx-section>

<dx-section name="check-button">
    <button hx-post="/showcase/simple/confirm">
        Confirm, {{ name }}
    </button>
</dx-section>

<dx-section name="check-confirmed">
    <button disabled>Confirmed!</button>
</dx-section>
"""


class SimpleInlineActionRouter(DXEndpointBattery):
    section_inline = TEMPLATE

    @dx_route("agreement", methods=["GET"])
    def get_agreement(self, request):
        # name parameter is not defined in dx_route; defaults to func.__name__
        return self.render_section(request, "agreement")

    @dx_route("get-check-button", methods=["GET"], name="load-check-button")
    def get_check_button(self, request):
        # name parameter of dx_route is defined overriding the func.__name__
        context = {"name": "Phil"}
        messages.info(request, "Ready for confirmation!")
        return self.render_section(
            request, section_name="check-button", context=context
        )

    @dx_route("confirm", methods=["PUT", "POST"])
    def confirm(self, request):
        # Using the django.contrib.messages framework - self.render_section will handle the swap oob injection
        messages.success(request, "Thanks for confirming!")
        return self.render_section(request, "check-confirmed")
