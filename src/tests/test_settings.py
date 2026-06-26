from django.test import override_settings
from djact.conf import package_settings as djact_settings


def test_conf_DX_HTMX_VERSION():
    assert djact_settings.DX_HTMX_VERSION == "4"
    with override_settings(DX_HTMX_VERSION="2"):
        assert djact_settings.DX_HTMX_VERSION == "2"


def test_conf_DX_SECTION_TAG():
    section_name = getattr(djact_settings, "DX_SECTION_TAG", None)
    assert section_name is not None
    assert section_name == "dx-section"
    with override_settings(DX_SECTION_TAG="my-section-tag"):
        section_name = getattr(djact_settings, "DX_SECTION_TAG", None)
        assert section_name is not None
        assert section_name == "my-section-tag"
