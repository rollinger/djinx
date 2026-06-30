from django.template import Library
from djxi.conf import package_settings as djxi_settings

register = Library()


@register.inclusion_tag("djxi/htmx_script.html")
def htmx_script_inclusion():
    minified = ".min" if djxi_settings.DX_HTMX_MINIFIED is True else ""
    version = djxi_settings.DX_HTMX_VERSION
    return {"version": version, "minified": minified}


@register.inclusion_tag("djxi/htmx_headers.html")
def htmx_headers():
    explicit_inheritance = djxi_settings.DX_HTMX_VERSION == "4"
    return {"explicit_inheritance": explicit_inheritance}


@register.inclusion_tag("djxi/messages/message_container.html")
def flash_messages_inclusion():
    return {
        "msg_container_id": djxi_settings.DX_MESSAGE_CONTAINER_ID,
        "msg_swap_method": djxi_settings.DX_MESSAGE_SWAP_METHOD,
        "msg_template": djxi_settings.DX_MESSAGE_TEMPLATE,
    }
