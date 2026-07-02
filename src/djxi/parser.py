from html.parser import HTMLParser
from djxi.conf import package_settings as djxi_settings
from djxi.error import (
    CircularIncludedSection,
    MissingIncludedSection,
    IncludeTagMissingName,
)


def parse_tag_attributes(attr_text: str):
    """
    Parse attributes from inside a start-tag string (text after the tag name).
    Returns a list of tuples: (name, value, quote_char) where value is None for
    boolean attrs, and quote_char is the outer quote used ('"' or "'"), or None
    if the value was unquoted.
    This is a small stateful tokenizer that avoids the HTMLParser's attr-splitting
    problems when attribute values contain nested quotes (e.g. Django tags).
    """
    i = 0
    n = len(attr_text)
    attrs = []
    while i < n:
        # skip whitespace
        while i < n and attr_text[i].isspace():
            i += 1
        if i >= n:
            break

        # read attribute name (allow letters, digits, -, :, _)
        start = i
        while i < n and (attr_text[i].isalnum() or attr_text[i] in "_-:"):
            i += 1
        name = attr_text[start:i]
        if not name:
            # stray character - skip it
            i += 1
            continue

        # skip whitespace
        while i < n and attr_text[i].isspace():
            i += 1

        value = None
        quote_char = None
        # if equals sign, parse value
        if i < n and attr_text[i] == "=":
            i += 1
            # skip whitespace after =
            while i < n and attr_text[i].isspace():
                i += 1
            if i < n and attr_text[i] in ('"', "'"):
                quote_char = attr_text[i]
                i += 1
                start_val = i
                # find matching outer quote; do not treat different inner quotes as terminator
                while i < n:
                    if attr_text[i] == quote_char:
                        break
                    i += 1
                value = attr_text[start_val:i]
                # advance past closing quote if present
                if i < n and attr_text[i] == quote_char:
                    i += 1
            else:
                # unquoted value: take until whitespace
                start_val = i
                while i < n and not attr_text[i].isspace():
                    i += 1
                value = attr_text[start_val:i]
        else:
            # boolean attribute (no value)
            value = None
            quote_char = None

        attrs.append((name, value, quote_char))
    return attrs


def attrs_to_string(attrs):
    """
    Reconstruct attribute string from list returned by parse_tag_attributes.
    Uses the original quote_char when available; otherwise prefers single quotes.
    """
    parts = []
    for name, value, quote_char in attrs:
        if value is None:
            parts.append(name)
        else:
            q = quote_char or "'"
            # if original quote is not available and q appears inside value, switch to the other quote
            if quote_char is None:
                if "'" in value and '"' not in value:
                    q = '"'
                elif "'" in value and '"' in value:
                    # both quotes present: escape double quotes for safety
                    q = '"'
                    val = value.replace('"', "&quot;")
                    parts.append(f"{name}={q}{val}{q}")
                    continue
            parts.append(f"{name}={q}{value}{q}")
    return " ".join(parts)


class SectionParser(HTMLParser):
    remainder_section_name = "re__main__der"

    def __init__(self):
        super().__init__()
        self.section_tag = getattr(djxi_settings, "DX_SECTION_TAG", None)
        self.sections = {self.remainder_section_name: ""}  # name -> inner HTML
        self._current_name = None
        self._inside = False
        self._chunks = []

    def _parse_attrs_from_starttag(self, tag: str):
        st = self.get_starttag_text() or ""
        prefix = f"<{tag}"
        inner = ""
        if st.startswith(prefix):
            inner = st[len(prefix) :].rstrip(">").strip()
            # strip trailing slash for self-closing like "<tag .../>"
            if inner.endswith("/"):
                inner = inner[:-1].rstrip()
        return parse_tag_attributes(inner)

    def handle_starttag(self, tag, attrs):
        if tag == self.section_tag:
            parsed = self._parse_attrs_from_starttag(tag)
            attrs_dict = {k: v for k, v, _ in parsed}
            name = attrs_dict.get("name")
            if name:
                self._current_name = name
                self._inside = True
                self._chunks = []
            return

        parsed = self._parse_attrs_from_starttag(tag)
        attrs_str = (" " + attrs_to_string(parsed)) if parsed else ""
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
        parsed = self._parse_attrs_from_starttag(tag)
        attrs_str = (" " + attrs_to_string(parsed)) if parsed else ""
        if tag == self.section_tag:
            # treat as section start+end: only record empty or provided name
            attrs_dict = {k: v for k, v, _ in parsed}
            name = attrs_dict.get("name")
            if name:
                self.sections[name] = ""
            return

        if self._inside:
            self._chunks.append(f"<{tag}{attrs_str}/>")
        else:
            self.sections[self.remainder_section_name] += f"<{tag}{attrs_str}/>"


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

    def _parse_attrs_from_starttag(self, tag: str):
        st = self.get_starttag_text() or ""
        prefix = f"<{tag}"
        inner = ""
        if st.startswith(prefix):
            inner = st[len(prefix) :].rstrip(">").strip()
            if inner.endswith("/"):
                inner = inner[:-1].rstrip()
        return parse_tag_attributes(inner)

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
                raise CircularIncludedSection(
                    f"Circular include detected for section '{name}'"
                )
            return ""

        content = self.cache.get(name)
        if content is None or content == "":
            if self.debug:
                raise MissingIncludedSection(f"Included section '{name}' not found")
            return ""

        # Use a fresh SectionExpander for nested expansion to avoid feeding while
        # already feeding on this parser instance.
        exp = SectionExpander(self.cache)
        return exp.expand(content, stack=self._current_stack + [name])

    def handle_starttag(self, tag, attrs):
        parsed = self._parse_attrs_from_starttag(tag)
        attrs_dict = {k: v for k, v, _ in parsed}
        if tag == self.include_tag:
            inc_name = attrs_dict.get("name")
            if inc_name:
                self.parts.append(self._expand_section(inc_name))
            else:
                # missing name attr -> treat as missing section
                if self.debug:
                    raise IncludeTagMissingName(
                        "dx-include tag missing 'name' attribute"
                    )
                # else skip silently
            return

        attrs_str = (" " + attrs_to_string(parsed)) if parsed else ""
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        if tag == self.include_tag:
            return
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    def handle_startendtag(self, tag, attrs):
        parsed = self._parse_attrs_from_starttag(tag)
        attrs_dict = {k: v for k, v, _ in parsed}
        if tag == self.include_tag:
            inc_name = attrs_dict.get("name")
            if inc_name:
                self.parts.append(self._expand_section(inc_name))
            else:
                if self.debug:
                    raise IncludeTagMissingName(
                        "dx-include tag missing 'name' attribute"
                    )
            return

        attrs_str = (" " + attrs_to_string(parsed)) if parsed else ""
        self.parts.append(f"<{tag}{attrs_str}/>")
