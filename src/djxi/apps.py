from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class DjxiAppConfig(AppConfig):
    name = "djxi"
    verbose_name = "Djxi"

    def ready(self):
        """
        Django calls this method when the application registry is fully loaded.
        This is the safest place to import signals, validators, or run
        one-time startup code.
        """
        # Validate required settings exist and are sane
        from .conf import package_settings

        htmx_version = package_settings.DX_HTMX_VERSION
        if htmx_version not in ["2", "4"]:
            raise ImproperlyConfigured("DX_HTMX_VERSION must be 2 or 4")

        section_tag = package_settings.DX_SECTION_TAG
        if not isinstance(section_tag, str) or section_tag == "":
            raise ImproperlyConfigured("DX_SECTION_TAG can not be None or empty")

        # Optional: Import signals if you have a signals.py file
        # import mypackage.signals
