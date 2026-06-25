""" Test compatibility of inline sections with Django Templating"""
from djxi.actions import DxActionRouter, dx_route
from django.test import override_settings, RequestFactory
from django.urls import path, include, resolve, reverse

INLINE_TEMPLATE = """
<dx-section name="hello-world">
    <p>Hello, {{name}}!</p>
</dx-section>
"""


class InlineActionRouter(DxActionRouter):
    inline_template = INLINE_TEMPLATE

    @dx_route("hello/<str:name>", methods=["GET"], name="hello_world")
    def hallo_du(self, request, name: str):
        context = {"name": name}
        return self.render_section(request, "hello-world", context)


# URL Patterns from .dx_router
urlpatterns = [
    path("", include((InlineActionRouter.dx_router(), "djxi"), namespace="djxi"))
]


@override_settings(ROOT_URLCONF=__name__)
def test_hallo_django():
    rf = RequestFactory()
    resolver_match = resolve(reverse("djxi:hello_world", kwargs={"name": "Django"}))
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>Hello, Django!</p>"
