from django.template import TemplateSyntaxError


class SectionIncludeError(TemplateSyntaxError):
    """Base exception for section include errors."""

    pass


class MissingIncludedSection(SectionIncludeError):
    """Raised when an included section is missing."""

    pass


class CircularIncludedSection(SectionIncludeError):
    """Raised when a circular include is detected."""

    pass


class IncludeTagMissingName(SectionIncludeError):
    """Raised when a dx-include tag is missing a 'name' attribute."""

    pass
