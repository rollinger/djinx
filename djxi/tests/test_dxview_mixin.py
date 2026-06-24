from src.djxi.actions.base import DjxiActionsMixin

TEMPLATE = """
<dx-section name="a-b">AB</dx-section><dx-section name="long spaced name">
Long spaced Name
</dx-section>

<dx-section name="b-c-d">
    This should be good<br>
</dx-section>
"""


class MyDxActionBattery(DjxiActionsMixin):
    dx_section_template = TEMPLATE


def test_dx_view_mixin_build_sections():
    dxview = MyDxActionBattery()
    assert len(dxview._dx_section_dict) == 3
    assert dxview.get_template_section("a-b") == "AB"
    assert dxview.get_template_section("long spaced name") == "\nLong spaced Name\n"
    assert dxview.get_template_section("b-c-d") == "\n    This should be good<br>\n"
    assert dxview.get_template_section("this-key-does-not_exist") == ""
