from djxi.actions import DxActionRouter
from django.test import override_settings

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


class InlineActionRouter(DxActionRouter):
    section_inline = INLINE_TEMPLATE


@override_settings(DX_SECTION_TAG=DEFAULT)
def test_default_section_tag():
    default_router = InlineActionRouter()
    assert len(default_router._dx_section_cache) == 3
    assert default_router.get_section("section_01") == "Content 1"
    assert default_router.get_section("section_02") == "Content 2"
    assert default_router.get_section("section_04") == "Content 4"


@override_settings(DX_SECTION_TAG=CUSTOM)
def test_custom_section_tag():
    custom_router = InlineActionRouter()
    assert len(custom_router._dx_section_cache) == 2
    assert custom_router.get_section("section_03") == "Content 3"
    assert custom_router.get_section("section_05") == "Content 5"
