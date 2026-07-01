from django.core.exceptions import ImproperlyConfigured

from djxi.parser import SectionParser, load_django_template


class DXSectionMixin:
    """Mixin of functionality to extract sections from templates and inline strings."""

    # TODO: Rename in inline_template and template_name to match Django convention.
    section_inline = None
    section_template_name = None

    def __init__(self, **kwargs):
        """Constructor builds the dx section cache."""
        if self.section_inline is None and self.section_template_name is None:
            raise ImproperlyConfigured(
                "DXEndpointBattery requires a definition of sections via "
                "'section_inline' or a path to a 'section_template_name'"
            )
        self.build_section_cache()

    def build_section_cache(self) -> None:
        """On init builds the section cache.
        A dictionary with the (k,v) = name-of-section, html_string.
        """
        self._dx_section_cache = self.parse_section_dict()

    def parse_section_dict(self) -> dict:
        """Parses the string and extract the dx-section parts."""
        parser = SectionParser()
        parser.feed(self.build_section_string())
        return parser.sections

    def build_section_string(self) -> str:
        """Concatenates the specified templates and returns the unmodified string.
        In most cases you want to set one or the other, yet both is allowed.
        Sections are read in order and later redefinition may override.
        """
        section_string = ""
        if self.section_template_name is not None:
            section_string = load_django_template(self.section_template_name)
        if self.section_inline is not None:
            section_string += self.section_inline
        return section_string

    def get_section(self, name: str) -> str:
        """Returns the djxi section from the _dx_section_cache.
        If name cannot be found, returns empty string.
        """
        return self._dx_section_cache.get(name, "")
