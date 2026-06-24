from django.conf import settings

# Define your package's default settings here.
# Use ALL CAPS names, just like Django's own settings.
DEFAULTS = {
    "DX_HTMX_VERSION": "4",
    "DX_SECTION_NAME": "dx-section",
}


class Settings:
    """
    A proxy object that reads from django.conf.settings first,
    and falls back to DEFAULTS if the user didn't define it.
    """

    def __getattr__(self, name):
        if name not in DEFAULTS:
            raise AttributeError(f"Invalid setting: '{name}'")

        # Return the user's value from settings.py, or fall back to the default
        return getattr(settings, name, DEFAULTS[name])


# Instantiate a single global object for easy import
package_settings = Settings()
