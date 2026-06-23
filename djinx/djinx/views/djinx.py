from django.shortcuts import render

TEMPLATE = """
<dx-section name="check-button">
    <div>Read this before confirm</div>
    <div hx-get="/get-check-button" hx-trigger="revealed" hx-swap="outerHTML">Loading...</div>
</dx-section>

<dx-section name="check-button">
    <button hx-post="/confirm">
        Confirm
    </button>
</dx-section>

<dx-section name="check-confirmed">
    <button disabled>Confirmed!</button>
</dx-section>
"""


class DjinxViewMixin:
    dx_section_template_name = TEMPLATE

    def __init__(self):
        self.build_dx_sections()
        return super().__init__()

    def build_dx_sections(self):
        """Called on class initialization."""
        self._dx_section_dict = {}

    def get_template_section(self, name: str) -> str:
        """Returns the dx-section template for this view.
        If name cannot be found, returns an empty string.
        """
        return self._dx_section_dict.get(name, "")

    # @route("/get-check-button", methods=["GET"])
    def get_check_button(self, request):
        context = {}
        return render(request, self.get_template_section("check-button"), context)

    # @route("/confirm", methods=["POST"])
    def confirm(self, request):
        context = {}
        return render(request, self.get_template_section("check-confirmed"), context)
