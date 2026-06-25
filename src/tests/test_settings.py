from djxi.conf import package_settings as djxi_settings


def test_conf_DX_SECTION_NAME():
    section_name = getattr(djxi_settings, "DX_SECTION_NAME", None)
    assert section_name is not None
    assert section_name == "dx-section"
