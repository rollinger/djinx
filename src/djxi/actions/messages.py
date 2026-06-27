from django.contrib.messages import get_messages

from djxi.actions.parser import load_django_template
from djxi.conf import package_settings as djxi_settings


def fetch_messages_template(request) -> str:
    """Checks if messages are in the request context and returns the message_template in the hx-partial format.
    Returns a string
    """
    message_template_str = ""
    storage = get_messages(request)
    if len(storage) > 0:
        message_template_str = f'<hx-partial hx-target="#{djxi_settings.DX_MESSAGE_CONTAINER_ID}" hx-swap="{djxi_settings.DX_MESSAGE_SWAP_METHOD}">'
        message_template_str += load_django_template(djxi_settings.DX_MESSAGE_TEMPLATE)
        message_template_str += "</hx-partial>"
    return message_template_str
