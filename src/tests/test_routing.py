# fmt: off
from django.test import override_settings, RequestFactory
from django.urls import path, include, resolve, reverse

from djact.actions import DxActionRouter, dx_route

INLINE_TEMPLATE = """
<dx-section name="section_01">Content 1</dx-section>
<dx-section name="section_02">Content 2</dx-section>
<dx-section name="section_03">Content 3</dx-section>
"""


class InlineActionRouter(DxActionRouter):
    section_inline = INLINE_TEMPLATE

    @dx_route("section/1", methods=["GET"], name="nifty_first_section")
    def section_01(self, request):
        return self.render_section(request, "section_01")

    @dx_route("section/2/", methods=["GET"])
    def section_02(self, request):
        return self.render_section(request, "section_02")

    @dx_route("section/3", methods=["GET", "POST"])
    def section_03(self, request):
        return self.render_section(request, "section_03")

    @dx_route("section/<int:id>", methods=["GET"], name="get_the_section_you_want")
    def section_by_id(self, request, id):
        section_name = f"section_{id}"
        return self.render_section(request, section_name)


# URL Patterns from .dx_router
urlpatterns = [
    path("", include((InlineActionRouter.dx_router(), "djact"), namespace="djact"))
]


@override_settings(ROOT_URLCONF=__name__)
def test_path_resolver():
    true_paths = {
        "/section/1": {"view": "section_01", "args": (), "kwargs": {}, "content": "Content 1"},
        "/section/2/": {"view": "section_02", "args": (), "kwargs": {}, "content": "Content 2"},
        "/section/3": {"view": "section_03", "args": (), "kwargs": {}, "content": "Content 3"},
        "/section/4": {"view": "section_by_id", "args": (), "kwargs": {"id": 4}, "content": ""},
        "/section/99": {"view": "section_by_id", "args": (), "kwargs": {"id": 99}, "content": ""},
    }
    rf = RequestFactory()
    for request_path, truth in true_paths.items():
        match = resolve(request_path)
        assert match.func.__name__ == truth["view"]
        assert match.args == truth["args"]
        assert match.kwargs == truth["kwargs"]
        req = rf.get(request_path)
        assert match.func(req, *match.args, **match.kwargs).content.decode() == truth["content"]

@override_settings(ROOT_URLCONF=__name__)
def test_name_resolver():
    request_path = reverse("djact:nifty_first_section")
    assert request_path == "/section/1"
    match = resolve(request_path)
    assert match.func.__name__ == "section_01"


@override_settings(ROOT_URLCONF=__name__)
def test_no_name_resolver():
    request_path = reverse("djact:section_02")
    assert request_path == "/section/2/"
    match = resolve(request_path)
    assert match.func.__name__ == "section_02"

@override_settings(ROOT_URLCONF=__name__)
def test_name_override_resolver():
    request_path = reverse("djact:get_the_section_you_want", kwargs={"id": 3})
    assert request_path == "/section/3"
    match = resolve(request_path)
    assert match.func.__name__ == "section_03"
    request_path = reverse("djact:get_the_section_you_want", kwargs={"id": 4})
    assert request_path == "/section/4"
    match = resolve(request_path)
    assert match.func.__name__ == "section_by_id"
