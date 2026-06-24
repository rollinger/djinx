from django.conf import settings

# Set the xml tag to use for djxi sections in templates
DX_SECTION_NAME = getattr(settings, "DX_SECTION_NAME", "dx-section")
