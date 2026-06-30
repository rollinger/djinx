from django.template import Library
from djxi.conf import package_settings as djxi_settings, HTMX_CDN_PATHS

register = Library()


@register.inclusion_tag("djxi/htmx_script.html")
def htmx_script_inclusion():
    version = djxi_settings.DX_HTMX_VERSION
    compression = djxi_settings.DX_HTMX_COMPRESSION
    cdn_path = HTMX_CDN_PATHS[version][compression]
    return {"htmx_cdn_path": cdn_path[0], "integrity": cdn_path[1]}


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
