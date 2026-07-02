from django.contrib.messages import get_messages

from djxi.loader import load_django_template
from djxi.conf import package_settings as djxi_settings


def fetch_messages_template(request) -> str:
    """Checks if messages are in the request context and returns the message_template in the hx-partial format.
    Returns a string containing the message list template as an unevaluated string wrapped in a div
    which will be swapped out-of-bands in the message container.
    """
    message_template_str = ""
    message_pipeline = get_messages(request)
    if len(message_pipeline) > 0:
        message_template_str += f"""
        <div hx-swap-oob="{djxi_settings.DX_MESSAGE_SWAP_METHOD}:#{djxi_settings.DX_MESSAGE_CONTAINER_ID}">
          {load_django_template(djxi_settings.DX_MESSAGE_TEMPLATE)}
        </div>
        """
    return message_template_str
