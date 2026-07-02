import os
from django.template import loader


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
