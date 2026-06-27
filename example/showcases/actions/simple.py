from djxi.actions import DxActionRouter, dx_route

TEMPLATE = """
<dx-section name="agreement">
    <div>Read this before confirm</div>
    <div hx-get="/showcase/simple/get-check-button" hx-trigger="revealed delay:1s" hx-swap="outerHTML">Loading...</div>
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


class SimpleInlineActionRouter(DxActionRouter):
    section_inline = TEMPLATE

    @dx_route("agreement", methods=["GET"])
    def agreement(self, request):
        return self.render_section(request, "agreement")

    @dx_route("get-check-button", methods=["GET"])
    def get_check_button(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="check-button", context=context
        )

    @dx_route("confirm", methods=["PUT", "POST"])
    def confirm(self, request):
        context = {}
        return self.render_section(request, "check-confirmed", context)
