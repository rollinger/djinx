import os
import re
from html.parser import HTMLParser
from django.template import loader

from djxi.conf import package_settings as djxi_settings


class VerbatimSectionParser(HTMLParser):
    remainder_section_name = "re__main__der"

    def __init__(self):
        super().__init__()
        self.section_tag = getattr(djxi_settings, "DX_SECTION_TAG", None)
        self.sections = {self.remainder_section_name: ""}  # name -> inner HTML

    def feed(self, data: str):
        """Accept the full template string and parse it, preserving raw characters
        outside section tags into the remainder entry."""
        self.sections = {self.remainder_section_name: ""}
        if not self.section_tag or not data:
            self.sections[self.remainder_section_name] = data or ""
            return

        s = data
        pos = 0
        tag = self.section_tag

        while True:
            start_index = s.find(f"<{tag}", pos)
            if start_index == -1:
                break

            # Ensure it's a real tag-like occurrence (next char is space, '/', or '>')
            after = start_index + 1 + len(tag)
            if after < len(s) and not (s[after].isspace() or s[after] in "/>"):
                pos = start_index + 1
                continue

            # Copy everything before the start tag verbatim to remainder
            self.sections[self.remainder_section_name] += s[pos:start_index]

            # Find the end of the start tag (skip quoted '>' chars)
            st_end = self._find_tag_end(s, start_index)
            start_tag_text = s[start_index : st_end + 1]

            name = self._extract_name_attr(start_tag_text)
            if not name:
                # Not a named section start; copy the start tag verbatim
                self.sections[self.remainder_section_name] += start_tag_text
                pos = st_end + 1
                continue

            # Find the corresponding end tag occurrence
            end_search_pos = st_end + 1
            end_index = s.find(f"</{tag}", end_search_pos)
            if end_index == -1:
                # No end tag: copy the rest verbatim and stop
                self.sections[self.remainder_section_name] += s[st_end + 1 :]
                pos = len(s)
                break

            end_tag_end = self._find_tag_end(s, end_index)
            inner = s[st_end + 1 : end_index]
            self.sections[name] = inner
            pos = end_tag_end + 1

        # Append any trailing text verbatim
        if pos < len(s):
            self.sections[self.remainder_section_name] += s[pos:]

    def _find_tag_end(self, s: str, start: int) -> int:
        """Return index of the closing '>' for a tag starting at `start`,
        skipping over quoted '>' characters."""
        i = start
        in_quote = None
        while i < len(s):
            ch = s[i]
            if in_quote:
                if ch == in_quote:
                    in_quote = None
            else:
                if ch == '"' or ch == "'":
                    in_quote = ch
                elif ch == ">":
                    return i
            i += 1
        return len(s) - 1

    def _extract_name_attr(self, tag_text: str):
        """Extract a `name` attribute value from a start tag text, if present."""
        m = re.search(r'\bname\s*=\s*(?P<q>["\'])(?P<v>.*?)(?P=q)', tag_text)
        if m:
            return m.group("v")
        m2 = re.search(r"\bname\s*=\s*([^\s>]+)", tag_text)
        if m2:
            return m2.group(1)
        return None


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
