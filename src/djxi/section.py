from django.core.exceptions import ImproperlyConfigured

from djxi.parser import SectionParser, load_django_template
from html.parser import HTMLParser


class DXSectionMixin:
    """Mixin of functionality to extract sections from templates and inline strings."""

    inline_template = None
    template_name = None

    def __init__(self, **kwargs):
        """Constructor builds the dx section cache."""
        if self.inline_template is None and self.template_name is None:
            raise ImproperlyConfigured(
                "DXSectionMixin requires a definition of sections via "
                "'inline_template' or a path to a 'template_name'"
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
        if self.template_name is not None:
            section_string = load_django_template(self.template_name)
        if self.inline_template is not None:
            section_string += self.inline_template
        return section_string

    def get_section(self, name: str) -> str:
        """Returns the djxi section from the _dx_section_cache.
        If name cannot be found, returns empty string.
        """
        return self._dx_section_cache.get(name, "")

    def get_section_included(self, name: str) -> str:
        """Returns the djxi section from the _dx_section_cache with <dx-include name="xyz"> expanded by the
        relevant section from the _dx_section_cache.
        """
        section = self.get_section(name)
        # Expand <dx-include name="..."> tags by inserting the referenced section
        # Preserve all other content exactly as-is (HTML, template tags, whitespace).

        cache = self._dx_section_cache

        def _expand(s: str, stack: set) -> str:
            parts = []

            class _Expander(HTMLParser):
                def handle_starttag(self, tag, attrs):
                    if tag == "dx-include":
                        attrs_dict = dict(attrs)
                        inc_name = attrs_dict.get("name")
                        if inc_name:
                            # avoid circular includes
                            if inc_name in stack:
                                return
                            stack.add(inc_name)
                            parts.append(_expand(cache.get(inc_name, ""), stack))
                            stack.remove(inc_name)
                        return

                    attrs_str = (
                        " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
                    )
                    parts.append(f"<{tag}{attrs_str}>")

                def handle_endtag(self, tag):
                    if tag == "dx-include":
                        return
                    parts.append(f"</{tag}>")

                def handle_data(self, data):
                    parts.append(data)

                def handle_startendtag(self, tag, attrs):
                    if tag == "dx-include":
                        attrs_dict = dict(attrs)
                        inc_name = attrs_dict.get("name")
                        if inc_name:
                            if inc_name in stack:
                                return
                            stack.add(inc_name)
                            parts.append(_expand(cache.get(inc_name, ""), stack))
                            stack.remove(inc_name)
                        return

                    attrs_str = (
                        " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
                    )
                    parts.append(f"<{tag}{attrs_str}/>")

            # run parser and return the assembled parts
            p = _Expander()
            p.feed(s)
            return "".join(parts)

        included_section = _expand(section, set([name]))
        return included_section
