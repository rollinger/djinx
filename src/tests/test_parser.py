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
