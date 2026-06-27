import pytest
from django.core.exceptions import ImproperlyConfigured
from ..djxi.actions import DxActionRouter

INLINE_TEMPLATE = """
<dx-section name="a-b">AB</dx-section><dx-section name="long spaced name">
Long spaced Name
</dx-section>

<dx-section name="b-c-d">
    This should be good<br>
</dx-section>
"""


class EmptyActionRouter(DxActionRouter):
    pass


class InlineActionRouter(DxActionRouter):
    section_inline = INLINE_TEMPLATE


class TemplateActionRouter(DxActionRouter):
    section_template_name = "template.html"


def test_djxi_empty_init():
    # Raise error if inline_template and template_name is not configured
    with pytest.raises(ImproperlyConfigured):
        dx_action = EmptyActionRouter()  # noqa: F841


def test_djxi_inline_build_sections():
    dx_action = InlineActionRouter()
    assert len(dx_action._dx_section_cache) == 3
    assert dx_action.get_section("a-b") == "AB"
    assert dx_action.get_section("long spaced name") == "\nLong spaced Name\n"
    assert dx_action.get_section("b-c-d") == "\n    This should be good<br>\n"
    assert dx_action.get_section("this-key-does-not_exist") == ""


def test_djxi_template_build_sections():
    dx_action = TemplateActionRouter()
    assert len(dx_action._dx_section_cache) == 3
    assert dx_action.get_section("a-b") == "AB"
    assert dx_action.get_section("long spaced name") == "\nLong spaced Name\n"
    assert dx_action.get_section("b-c-d") == "\n    This should be good<br>\n"
    assert dx_action.get_section("this-key-does-not_exist") == ""
