from django.shortcuts import render

from .base import DjinxEndpointMixin
from .route import route

TEMPLATE = """
<dx-section name="agreement">
    <div>Read this before confirm</div>
    <div hx-get="get-check-button" hx-trigger="revealed" hx-swap="outerHTML">Loading...</div>
</dx-section>

<dx-section name="check-button">
    <button hx-post="confirm">
        Confirm
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
        return render(request, self.get_template_section("agreement"))

    @route("get-check-button", methods=["GET"])
    def get_check_button(self, request):
        context = {}
        return render(request, self.get_template_section("check-button"), context)

    @route("confirm", methods=["POST"])
    def confirm(self, request):
        context = {}
        return render(request, self.get_template_section("check-confirmed"), context)
