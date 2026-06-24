from html.parser import HTMLParser


class SectionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sections = {}  # name -> inner HTML
        self._current_name = None
        self._inside = False
        self._chunks = []

    def handle_starttag(self, tag, attrs):
        if tag == "dx-section":
            # Extract the 'name' attribute
            attrs_dict = dict(attrs)
            name = attrs_dict.get("name")
            if name:
                self._current_name = name
                self._inside = True
                self._chunks = []
            return
        if self._inside:
            # Re‑emit the opening tag (including its attributes)
            attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
            self._chunks.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        if tag == "dx-section" and self._inside:
            # End of section – store the collected inner HTML
            self.sections[self._current_name] = "".join(self._chunks)
            self._inside = False
            self._current_name = None
            self._chunks = []
        elif self._inside:
            # Re‑emit the closing tag for nested elements
            self._chunks.append(f"</{tag}>")

    def handle_data(self, data):
        if self._inside:
            self._chunks.append(data)

    def handle_startendtag(self, tag, attrs):
        # Self‑closing tags (like <br/> or <img ... />)
        if self._inside:
            attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in attrs) if attrs else ""
            self._chunks.append(f"<{tag}{attrs_str}/>")


# def compile_section_dict(html_string: str) -> dict:
#     """
#     Parse HTML containing <dx-section name="..."> ... </dx-section> blocks.
#     Returns a dict {name: inner_HTML} for each section.
#     Works with malformed HTML, unclosed tags, and multiple top‑level sections.
#     """
#     parser = SectionParser()
#     parser.feed(html_string)
#     return parser.sections
