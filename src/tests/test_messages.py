from django.http import HttpRequest

from djxi.messages import fetch_messages_template


def test_fetch_messages_template():
    request = HttpRequest()
    empty_str = fetch_messages_template(request)
    assert empty_str == ""
    # Fake a message without the message overhead
    setattr(request, "_messages", ["HAS", "SOME", "MESSAGES"])
    non_empty_str = fetch_messages_template(request)
    assert non_empty_str != ""
    assert non_empty_str.strip().startswith("<div hx-swap-oob") is True
    assert non_empty_str.strip().endswith("</div>") is True
