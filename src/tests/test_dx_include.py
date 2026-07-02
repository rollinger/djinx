from djxi.endpoint import DXEndpointBattery
from django.test import override_settings
import pytest
from djxi.error import (
    MissingIncludedSection,
    CircularIncludedSection,
    IncludeTagMissingName,
)

INLINE_TEMPLATE = """
Non section stuff
<dx-section name="outer1">
Outer: {% for i in [1,2,3] %}<dx-include name="inner1">{% endfor %}
</dx-section>
Non section stuff
<dx-section name="outer2">
Outer: {% for i in [1,2,3] %}<dx-include name="inner2">{% endfor %}
</dx-section>
<dx-section name="inner1">Inner1</dx-section>
<dx-section name="inner2">Inner2: {% for i in [1,2,3] %}<dx-include name="inner3">{% endfor %}</dx-section>
<dx-section name="inner3">Inner3</dx-section>
Non section stuff
"""


class DXIncludeBattery(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE


def test_djxi_included_sections():
    dx_include = DXIncludeBattery()
    # Base expansion
    assert (
        dx_include.get_section("outer1")
        == '\nOuter: {% for i in [1,2,3] %}<dx-include name="inner1">{% endfor %}\n'
    )
    assert (
        dx_include.get_section_included("outer1")
        == "\nOuter: {% for i in [1,2,3] %}Inner1{% endfor %}\n"
    )
    # Deep expansion
    assert (
        dx_include.get_section("outer2")
        == '\nOuter: {% for i in [1,2,3] %}<dx-include name="inner2">{% endfor %}\n'
    )
    assert dx_include.get_section_included("outer2") == (
        "\nOuter: {% for i in [1,2,3] %}Inner2: {% for i in [1,2,3] %}Inner3{% endfor %}{% endfor %}\n"
    )


def test_missing_include_non_debug():
    # Missing included section should be skipped silently when DEBUG is False
    inline = '<dx-section name="outer">A<dx-include name="noexist"/>B</dx-section>'

    class T(DXEndpointBattery):
        inline_template = inline

    t = T()
    assert t.get_section("outer") == 'A<dx-include name="noexist"/>B'
    assert t.get_section_included("outer") == "AB"


@override_settings(DEBUG=True)
def test_missing_include_debug_raises():
    # Missing included section should raise in debug mode
    inline = '<dx-section name="outer">A<dx-include name="noexist"/>B</dx-section>'

    class T(DXEndpointBattery):
        inline_template = inline

    t = T()
    with pytest.raises(MissingIncludedSection):
        t.get_section_included("outer")


def test_circular_includes_behavior():
    # Circular includes should raise in debug and skip in non-debug
    inline = (
        '<dx-section name="a">Start:<dx-include name="b"/></dx-section>'
        '<dx-section name="b">Mid:<dx-include name="a"/></dx-section>'
    )

    class T(DXEndpointBattery):
        inline_template = inline

    # Non-debug: should not raise but circular include results in skipping
    t = T()
    # Expect expansion: a -> Start: + expansion of b -> Mid: + expansion of a (skipped) => "Start:Mid:"
    assert t.get_section_included("a") == "Start:Mid:"

    # Debug: raising
    @override_settings(DEBUG=True)
    def _debug_run():
        t2 = T()
        with pytest.raises(CircularIncludedSection):
            t2.get_section_included("a")

    _debug_run()


def test_include_missing_name_attr():
    inline = '<dx-section name="outer">X<dx-include/>Y</dx-section>'

    class T(DXEndpointBattery):
        inline_template = inline

    # Non-debug: skip silently
    t = T()
    assert t.get_section_included("outer") == "XY"

    # Debug: raise
    @override_settings(DEBUG=True)
    def _debug():
        t2 = T()
        with pytest.raises(IncludeTagMissingName):
            t2.get_section_included("outer")

    _debug()


def test_custom_include_tag_setting():
    # Use a custom include tag name via settings
    inline = '<dx-section name="outer">Before:<my-include name="inner"/>:After</dx-section><dx-section name="inner">IN</dx-section>'

    class T(DXEndpointBattery):
        inline_template = inline

    with override_settings(DX_INCLUDE_TAG="my-include"):
        t = T()
        assert t.get_section_included("outer") == "Before:IN:After"
