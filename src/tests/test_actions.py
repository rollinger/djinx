import os
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured
from ..djxi.actions import DxActionRouter

TEST_DIR = Path(__file__).parent
TEMPLATE_PATH = os.path.join(Path(__file__).parent, "data/template.html")

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
    inline_template = INLINE_TEMPLATE


class TemplateActionRouter(DxActionRouter):
    template_name = TEMPLATE_PATH


def test_template_exists():
    template_path = os.path.join(TEST_DIR, TEMPLATE_PATH)
    assert os.path.exists(template_path)
    assert os.path.isfile(template_path)


def test_djxi_empty_init():
    # Raise error if inline_template and template_name is not configured
    with pytest.raises(ImproperlyConfigured):
        dx_action = EmptyActionRouter()  # noqa: F841


def test_djxi_inline_build_sections():
    dx_action = InlineActionRouter()
    assert len(dx_action._dx_section_dict) == 3
    assert dx_action.get_template_section("a-b") == "AB"
    assert dx_action.get_template_section("long spaced name") == "\nLong spaced Name\n"
    assert dx_action.get_template_section("b-c-d") == "\n    This should be good<br>\n"
    assert dx_action.get_template_section("this-key-does-not_exist") == ""


def test_djxi_template_build_sections():
    dx_action = TemplateActionRouter()
    assert len(dx_action._dx_section_dict) == 3
    assert dx_action.get_template_section("a-b") == "AB"
    assert dx_action.get_template_section("long spaced name") == "\nLong spaced Name\n"
    assert dx_action.get_template_section("b-c-d") == "\n    This should be good<br>\n"
    assert dx_action.get_template_section("this-key-does-not_exist") == ""
