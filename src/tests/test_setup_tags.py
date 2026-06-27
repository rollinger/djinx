from django.test import override_settings

from djxi.conf import package_settings as djxi_settings
from djxi.templatetags.djxi import htmx_script_inclusion, htmx_headers


def test_htmx_script_inclusion():
    # htmx4.js
    tag = htmx_script_inclusion()
    assert djxi_settings.DX_HTMX_VERSION == "4"
    assert djxi_settings.DX_HTMX_MINIFIED is False
    assert tag["minified"] == ""
    assert tag["version"] == djxi_settings.DX_HTMX_VERSION
    # Older version htmx2.min.js
    with override_settings(DX_HTMX_VERSION="2", DX_HTMX_MINIFIED=True):
        tag = htmx_script_inclusion()
        assert djxi_settings.DX_HTMX_VERSION == "2"
        assert djxi_settings.DX_HTMX_MINIFIED is True
        assert tag["minified"] == ".min"


def test_htmx_headers():
    # htmx 4 header style
    tag = htmx_headers()
    assert tag["explicit_inheritance"] is True
    # htmx 2 header style
    with override_settings(DX_HTMX_VERSION="2"):
        tag = htmx_headers()
        assert tag["explicit_inheritance"] is False
