from src.djxi.actions.base import DjinxEndpointMixin
from src.djxi.actions.route import route

TEMPLATE = """
<dx-section name="agreement">
    <div>Read this before confirm</div>
    <div hx-get="dx/get-check-button" hx-trigger="revealed delay:1s" hx-swap="outerHTML">Loading...</div>
</dx-section>

<dx-section name="check-button">
    <button hx-post="/dx/confirm">
        Confirm, {{ name }}
    </button>
</dx-section>

<dx-section name="check-confirmed">
    <button disabled>Confirmed!</button>
</dx-section>
"""


class MyDjinxBattery(DjinxEndpointMixin):
    dx_section_template = TEMPLATE

    @route("agreement", methods=["GET"])
    def agreement(self, request):
        return self.render_section(request, "agreement")

    @route("get-check-button", methods=["GET"])
    def get_check_button(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="check-button", context=context
        )

    @route("confirm", methods=["PUT", "POST"])
    def confirm(self, request):
        context = {}
        return self.render_section(request, "check-confirmed", context)
