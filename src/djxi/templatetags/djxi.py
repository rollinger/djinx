from django.template import Library
from djxi.conf import package_settings as djxi_settings

register = Library()


@register.inclusion_tag("htmx_script.html")
def htmx_script_inclusion():
    minified = ".min" if djxi_settings.DX_HTMX_MINIFIED is True else ""
    return {"version": djxi_settings.DX_HTMX_VERSION, "minified": minified}


@register.inclusion_tag("htmx_headers.html")
def htmx_headers():
    explicit_inheritance = djxi_settings.DX_HTMX_VERSION == "4"
    return {"explicit_inheritance": explicit_inheritance}
