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
    # TODO: REfactor into better name: load_django_template_string
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
