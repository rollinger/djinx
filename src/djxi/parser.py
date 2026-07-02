import os
from html.parser import HTMLParser
from django.template import loader

from djxi.conf import package_settings as djxi_settings


class SectionParser(HTMLParser):
    remainder_section_name = "re__main__der"

    def __init__(self):
        super().__init__()
        self.section_tag = getattr(djxi_settings, "DX_SECTION_TAG", None)
        self.sections = {self.remainder_section_name: ""}  # name -> inner HTML
        self._current_name = None
        self._inside = False
        self._chunks = []

    def handle_starttag(self, tag, attrs):
        if tag == self.section_tag:
            attrs_dict = dict(attrs)
            name = attrs_dict.get("name")
            if name:
                self._current_name = name
                self._inside = True
                self._chunks = []
            return

        attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
        if self._inside:
            self._chunks.append(f"<{tag}{attrs_str}>")
        else:
            self.sections[self.remainder_section_name] += f"<{tag}{attrs_str}>"

    def handle_endtag(self, tag):
        if tag == self.section_tag and self._inside:
            self.sections[self._current_name] = "".join(self._chunks)
            self._inside = False
            self._current_name = None
            self._chunks = []
            return

        if self._inside:
            self._chunks.append(f"</{tag}>")
        else:
            self.sections[self.remainder_section_name] += f"</{tag}>"

    def handle_data(self, data):
        if self._inside:
            self._chunks.append(data)
        else:
            self.sections[self.remainder_section_name] += data

    def handle_startendtag(self, tag, attrs):
        attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
        if self._inside:
            self._chunks.append(f"<{tag}{attrs_str}/>")
        else:
            self.sections[self.remainder_section_name] += f"<{tag}{attrs_str}/>"


def load_django_template(template_name: str) -> str:
    """Loads a Django template from the given name."""
    # TODO: Refactor into better name: load_django_template_string
    template_string = ""
    # If template_name references a filesystem path, read it directly.
    # In that case template name has to be an absolute path (this is mainly for the test suite)
    if os.path.exists(template_name):
        with open(template_name, "r", encoding="utf-8") as f:
            template_string = f.read()
    else:
        # Attempt to load via Django's template loader (e.g. app/template.html).
        try:
            tpl = loader.get_template(template_name)
            origin = getattr(tpl, "origin", None)
            if origin and hasattr(origin, "loader"):
                template_string = origin.loader.get_contents(origin)
            else:
                template_string = (
                    getattr(getattr(tpl, "template", None), "source", "") or ""
                )
        except Exception:
            template_string = ""
    return template_string


class SectionExpander(HTMLParser):
    """Expand <dx-include name="..."></dx-include> markers using a section cache.

    Behavior:
    - Uses DX_INCLUDE_TAG from package settings to find include tags.
    - On circular include or missing referenced section: raises RuntimeError if
      Django DEBUG is True, otherwise silently skips (inserts empty string).
    - Expansion is recursive and isolated by instantiating a fresh parser for
      each included section to keep parser state clean.
    """

    def __init__(self, cache: dict):
        super().__init__()
        from djxi.conf import package_settings as djxi_settings
        from django.conf import settings as _dj_settings

        self.cache = cache
        self.include_tag = getattr(djxi_settings, "DX_INCLUDE_TAG", "dx-include")
        self.debug = getattr(_dj_settings, "DEBUG", False)
        self.parts = []
        # stack is local to each expand() invocation; kept for clarity

    def expand(self, s: str, stack=None) -> str:
        """Expand includes in string s. `stack` is a list of section names
        currently being expanded (to detect cycles).
        """
        if stack is None:
            stack = []
        # Initialize parts fresh for this run
        self.parts = []
        # Store current stack for nested expansions via self._expand_section
        self._current_stack = list(stack)
        self.feed(s)
        return "".join(self.parts)

    def _expand_section(self, name: str) -> str:
        # detect cycle
        if name in self._current_stack:
            if self.debug:
                raise RuntimeError(f"Circular include detected for section '{name}'")
            return ""

        content = self.cache.get(name)
        if content is None or content == "":
            if self.debug:
                raise RuntimeError(f"Included section '{name}' not found")
            return ""

        # Use a fresh SectionExpander for nested expansion to avoid feeding while
        # already feeding on this parser instance.
        exp = SectionExpander(self.cache)
        return exp.expand(content, stack=self._current_stack + [name])

    def handle_starttag(self, tag, attrs):
        if tag == self.include_tag:
            attrs_dict = dict(attrs)
            inc_name = attrs_dict.get("name")
            if inc_name:
                self.parts.append(self._expand_section(inc_name))
            else:
                # missing name attr -> treat as missing section
                if self.debug:
                    raise RuntimeError("dx-include tag missing 'name' attribute")
                # else skip silently
            return

        attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        if tag == self.include_tag:
            return
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        if tag == self.include_tag:
            attrs_dict = dict(attrs)
            inc_name = attrs_dict.get("name")
            if inc_name:
                self.parts.append(self._expand_section(inc_name))
            else:
                if self.debug:
                    raise RuntimeError("dx-include tag missing 'name' attribute")
            return

        attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
        self.parts.append(f"<{tag}{attrs_str}/>")
