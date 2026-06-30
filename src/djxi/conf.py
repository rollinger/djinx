from django.conf import settings

# Define your package's default settings here.
# Use ALL CAPS names, just like Django's own settings.
DEFAULTS = {
    # Base Settings
    "DX_HTMX_VERSION": "4",  # allow ['2', '4']
    "DX_HTMX_COMPRESSION": ".js",  # allow: ['.js','.min.js']
    "DX_SECTION_TAG": "dx-section",
    # Messaging integration
    "DX_MESSAGE_CONTAINER_ID": "message-container",
    "DX_MESSAGE_SWAP_METHOD": "beforeend",
    "DX_MESSAGE_TEMPLATE": "djxi/messages/message_list.html",
}

HTMX_CDN_PATHS = {
    "2": {
        ".js": (
            "htmx.org@2.0.10/dist/htmx.js",
            "sha256-c5SYIE7T1Dejf9XKPRaxvaFOO5M1PqdEDH8Sm9C/k9U=",
        ),
        ".min.js": (
            "htmx.org@2.0.10/dist/htmx.min.js",
            "sha256-cepnGFv6jJjDnTFxfG/OXYUjcPzf0SnbRUN3TTFFwN4=",
        ),
    },
    "4": {
        ".js": (
            "htmx.org@4.0.0-beta5/dist/htmx.js",
            "sha256-UwmtmvzdgHwYPL81qVMWAvooSSuNJdDAfNtqDMXTBLw=",
        ),
        ".min.js": (
            "htmx.org@4.0.0-beta5/dist/htmx.min.js",
            "sha256-GS0tQl3aaDS9FZc6EPVZQM6iF6OoQPP4Gf/RYGO+mmg=",
        ),
    },
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
