import pytest
import types
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from djxi.apps import DjxiAppConfig
from djxi.conf import package_settings as djxi_settings


def test_conf_DX_HTMX_VERSION():
    assert djxi_settings.DX_HTMX_VERSION == "4"
    with override_settings(DX_HTMX_VERSION="2"):
        assert djxi_settings.DX_HTMX_VERSION == "2"


def test_conf_DX_SECTION_TAG():
    section_name = getattr(djxi_settings, "DX_SECTION_TAG", None)
    assert section_name is not None
    assert section_name == "dx-section"
    with override_settings(DX_SECTION_TAG="my-section-tag"):
        section_name = getattr(djxi_settings, "DX_SECTION_TAG", None)
        assert section_name is not None
        assert section_name == "my-section-tag"


def test_app_ready_checks():
    mod = types.ModuleType("djxi")
    mod.__file__ = __file__
    app = DjxiAppConfig("djxi", mod)
    with pytest.raises(ImproperlyConfigured):
        # Test HTMX VERSION
        with override_settings(DX_HTMX_VERSION="99"):
            app.ready()
        # Test compress level
        with override_settings(DX_HTMX_COMPRESSION=".bs.gz"):
            app.ready()
        # Test Section Tag
        with override_settings(DX_SECTION_TAG=""):
            app.ready()
        with override_settings(DX_SECTION_TAG=None):
            app.ready()
        with override_settings(DX_SECTION_TAG=99):
            app.ready()
