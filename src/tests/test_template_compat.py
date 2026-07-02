""" Test compatibility of inline sections with Django Templating Tags and Filter"""
from django.test import override_settings, RequestFactory, modify_settings
from django.urls import path, include, resolve, reverse

from djxi.endpoint import DXEndpointBattery
from djxi.router import dx_action

INLINE_TEMPLATE = """
<dx-section name="hello-world">
    <p>Hello, {{ name }}!</p>
</dx-section>
<dx-section name="hello-many">
    <p>Hello {% for name in names %}{{ name }}{% if not forloop.last %}, {% endif %}{% endfor %}!</p>
</dx-section>
<dx-section name="hello-filter">
    <p>{{ number|floatformat:3 }}</p>
</dx-section>
<dx-section name="hello-humanize">
    {% load humanize %}
    <p>{{ number|intword }}</p>
</dx-section>
<dx-section name="hello-include">
    <p>Hello {% for name in names %}{% include "partial.html" %}{% endfor %}!</p>
</dx-section>

"""


class InlineActionRouter(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE

    @dx_action("hello/<str:name>", methods=["GET"], name="hello_world")
    def hallo_du(self, request, name: str):
        context = {"name": name}
        return self.render_section(request, "hello-world", context)

    @dx_action("hello-all", methods=["GET"], name="hello_many")
    def hello_many(self, request):
        context = {"names": ["Django", "World", "Python"]}
        return self.render_section(request, "hello-many", context)

    @dx_action("hello-filter/<str:number>", methods=["GET"])
    def hello_filter(self, request, number: str):
        context = {"number": number}
        return self.render_section(request, "hello-filter", context)

    @dx_action("hello-humanize/<str:number>", methods=["GET"])
    def hello_humanize(self, request, number: str):
        return self.render_section(request, "hello-humanize", {"number": number})

    @dx_action("hello_include", methods=["GET"])
    def hello_include(self, request):
        context = {"names": ["Django", "World", "Python"]}
        return self.render_section(request, "hello-include", context)


# URL Patterns from .url_patterns
urlpatterns = [
    path("", include((InlineActionRouter.url_patterns(), "djxi"), namespace="djxi"))
]


@override_settings(ROOT_URLCONF=__name__)
def test_value_interpolation():
    rf = RequestFactory()
    resolver_match = resolve(reverse("djxi:hello_world", kwargs={"name": "Django"}))
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>Hello, Django!</p>"


@override_settings(ROOT_URLCONF=__name__)
def test_builtin_templatetags():
    rf = RequestFactory()
    resolver_match = resolve(reverse("djxi:hello_many"))
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>Hello Django, World, Python!</p>"


@override_settings(ROOT_URLCONF=__name__)
def test_template_include():
    rf = RequestFactory()
    resolver_match = resolve(reverse("djxi:hello_include"))
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>Hello Django & World & Python!</p>"


@override_settings(ROOT_URLCONF=__name__)
def test_buildin_filter():
    rf = RequestFactory()
    resolver_match = resolve(
        reverse("djxi:hello_filter", kwargs={"number": "108.999212"})
    )
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>108.999</p>"


@modify_settings(INSTALLED_APPS={"append": "django.contrib.humanize"})
@override_settings(ROOT_URLCONF=__name__)
def test_opt_in_tags():
    rf = RequestFactory()
    resolver_match = resolve(
        reverse("djxi:hello_humanize", kwargs={"number": "1000000"})
    )
    req = rf.get(resolver_match.url_name)
    response = resolver_match.func(req, *resolver_match.args, **resolver_match.kwargs)
    assert req.method == "GET"
    assert response.status_code == 200
    assert response.content.decode().strip() == "<p>1.0 million</p>"
