from django.contrib import messages
from django.views.generic import TemplateView


class ShowcasesIndexView(TemplateView):
    template_name = "showcases/list.html"

    def get(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.INFO,
            "This is a message from the default messaging framework.",
        )
        return super().get(request, *args, **kwargs)
