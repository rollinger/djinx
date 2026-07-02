from django.test import override_settings
from django.urls import path, include, resolve

from djxi.endpoint import DXEndpointBattery
from djxi.router import (
    dx_get,
    dx_post,
    dx_put,
    dx_patch,
    dx_delete,
)


class InlineActionRouter(DXEndpointBattery):
    inline_template = """<dx-section name="section_01">Content 1</dx-section>"""

    @dx_get("act/get/", name="get-stuff")
    def action_get(self, request):
        return self.render_section(request, "section_01")

    @dx_post("act/post/", name="post-stuff")
    def action_post(self, request):
        return self.render_section(request, "section_01")

    @dx_put("act/put/", name="put-stuff")
    def action_put(self, request):
        return self.render_section(request, "section_01")

    @dx_patch("act/patch/", name="patch-stuff")
    def action_patch(self, request):
        return self.render_section(request, "section_01")

    @dx_delete("act/delete/", name="delete-stuff")
    def action_delete(self, request):
        return self.render_section(request, "section_01")


urlpatterns = [
    path("", include((InlineActionRouter.url_patterns(), "djxi"), namespace="djxi"))
]


@override_settings(ROOT_URLCONF=__name__)
def test_path_resolver():
    true_methods = {
        "/act/get/": {"view": "action_get", "method": ["GET"], "content": "Content 1"},
        "/act/post/": {
            "view": "action_post",
            "method": ["POST"],
            "content": "Content 1",
        },
        "/act/put/": {"view": "action_put", "method": ["PUT"], "content": "Content 1"},
        "/act/patch/": {
            "view": "action_patch",
            "method": ["PATCH"],
            "content": "Content 1",
        },
        "/act/delete/": {
            "view": "action_delete",
            "method": ["DELETE"],
            "content": "Content 1",
        },
    }
    for request_path, truth in true_methods.items():
        match = resolve(request_path)
        assert match.func.__name__ == truth["view"]
        assert match.func._dx_routes[0][1] == truth["method"]
