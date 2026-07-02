from django.contrib import messages
from djxi.endpoint import DXEndpointBattery
from djxi.router import dx_action


class ParameterInlineActionRouter(DXEndpointBattery):
    # Using a template instead of an inline string
    template_name = "showcases/sections/counter.html"

    @dx_action("counter", methods=["GET"])
    def counter(self, request):
        context = {"value": 1}
        return self.render_section(request, "counter", context)

    @dx_action("count/up/<int:value>", methods=["PUT"])
    def count_up(self, request, value):
        value += value
        context = {"value": value}
        if value > 100:
            messages.add_message(
                request, messages.WARNING, "The counter exceeded the limit of 100"
            )
            return self.render_section(request, "counter-exceeded", context)
        else:
            return self.render_section(request, "counter", context)
