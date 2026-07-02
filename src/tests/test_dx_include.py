from djxi.endpoint import DXEndpointBattery

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
    assert len(dx_include._dx_section_cache) == 6
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
