from django.test import override_settings
from djxi.endpoint import DXEndpointBattery

DEFAULT = "dx-section"
CUSTOM = "my-section-tag"

INLINE_TEMPLATE = f"""
<unrelated-tag>
<{DEFAULT} name="section_01">Content 1</{DEFAULT}>
<{DEFAULT} name="section_02">Content 2</{DEFAULT}>
<unrelated-tag/ >
<{CUSTOM} name="section_03">Content 3</{CUSTOM}>
<{DEFAULT} name="section_04">Content 4</{DEFAULT}>
<unrelated-tag>XYZ</unrelated-tag>
<{CUSTOM} name="section_05">Content 5</{CUSTOM}>
"""


class InlineActionRouter(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE


@override_settings(DX_SECTION_TAG=DEFAULT)
def test_default_section_tag():
    default_router = InlineActionRouter()
    assert len(default_router._dx_section_cache) == 4
    assert default_router.get_section("section_01") == "Content 1"
    assert default_router.get_section("section_02") == "Content 2"
    assert default_router.get_section("section_04") == "Content 4"
    assert (
        default_router.get_section("re__main__der")
        == '\n<unrelated-tag>\n\n\n<unrelated-tag>\n<my-section-tag name="section_03">Content 3</my-section-tag>\n\n<unrelated-tag>XYZ</unrelated-tag>\n<my-section-tag name="section_05">Content 5</my-section-tag>\n'
    )


@override_settings(DX_SECTION_TAG=CUSTOM)
def test_custom_section_tag():
    custom_router = InlineActionRouter()
    assert len(custom_router._dx_section_cache) == 3
    assert custom_router.get_section("section_03") == "Content 3"
    assert custom_router.get_section("section_05") == "Content 5"
    assert (
        custom_router.get_section("re__main__der")
        == '\n<unrelated-tag>\n<dx-section name="section_01">Content 1</dx-section>\n<dx-section name="section_02">Content 2</dx-section>\n<unrelated-tag>\n\n<dx-section name="section_04">Content 4</dx-section>\n<unrelated-tag>XYZ</unrelated-tag>\n\n'
    )


# New tests to cover Django-tag-containing attributes and boolean attributes
DJANGO_ATTR_TEMPLATE = """
<root>
  <div>
    <input type="search" name="search" value="{{search}}" autofocus hx-post='{% url "todo:list" %}' hx-trigger="input changed delay:200ms, keyup[key=='Enter']" hx-target="#todo-list_container">
  </div>
</root>
"""


class InlineDjangoAttrRouter(DXEndpointBattery):
    inline_template = DJANGO_ATTR_TEMPLATE


@override_settings(DX_SECTION_TAG=DEFAULT)
def test_django_tag_attribute_and_boolean_preserved():
    r = InlineDjangoAttrRouter()
    rem = r.get_section("re__main__der")
    # boolean attribute should be present as a boolean attribute
    assert "autofocus" in rem
    assert 'autofocus="None"' not in rem
    # hx-post should contain the Django tag intact with inner double quotes preserved
    assert "hx-post='{% url \"todo:list\" %}'" in rem
    # hx-trigger should preserve the inner single quotes around 'Enter'
    assert "keyup[key=='Enter']" in rem


# Extra test: self-closing tag with django tag inside attribute
SELF_CLOSING_TEMPLATE = """
<root>
  <img src="/x.png" data-url='{% url "todo:detail" pk=1 %}'/>
</root>
"""


class InlineSelfClosingRouter(DXEndpointBattery):
    inline_template = SELF_CLOSING_TEMPLATE


@override_settings(DX_SECTION_TAG=DEFAULT)
def test_self_closing_with_django_attr():
    r = InlineSelfClosingRouter()
    rem = r.get_section("re__main__der")
    assert "data-url='{% url \"todo:detail\" pk=1 %}'" in rem
