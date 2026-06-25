from django.test import override_settings
from django.urls import path, include, resolve

from djxi.actions import DxActionRouter, dx_route

INLINE_TEMPLATE = """
<dx-section name="section_01">Content 1</dx-section>
<dx-section name="section_02">Content 2</dx-section>
<dx-section name="section_03">Content 3</dx-section>
"""


class InlineActionRouter(DxActionRouter):
    inline_template = INLINE_TEMPLATE

    @dx_route("section/1", methods=["GET"])
    def section_01(self, request):
        return self.render_section(request, "section_01")

    @dx_route("section/2/", methods=["GET"])
    def section_02(self, request):
        return self.render_section(request, "section_02")

    @dx_route("section/3", methods=["POST"])
    def section_03(self, request):
        return self.render_section(request, "section_03")

    @dx_route("section/<int:id>", methods=["GET"])
    def section_by_id(self, request, id):
        section_name = f"section_{id}"
        return self.render_section(request, section_name)


# URL Patterns from .dx_router
urlpatterns = [
    path("", include((InlineActionRouter.dx_router(), "djxi"), namespace="djxi"))
]


@override_settings(ROOT_URLCONF=__name__)
def test_path_resolver():
    true_paths = {
        "/section/1": {"view": "section_01", "args": (), "kwargs": {}},
        "/section/2/": {"view": "section_02", "args": (), "kwargs": {}},
        "/section/3": {"view": "section_03", "args": (), "kwargs": {}},
    }
    for request_path, truth in true_paths.items():
        match = resolve(request_path)
        assert match.func.__name__ == truth["view"]
        assert match.args == truth["args"]
        assert match.kwargs == truth["kwargs"]
