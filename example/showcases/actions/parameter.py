from djxi.actions import DxActionRouter, dx_route


class ParameterInlineActionRouter(DxActionRouter):
    # Using a template instead of an inline string
    section_template_name = "showcases/sections/counter.html"

    @dx_route("counter", methods=["GET"])
    def counter(self, request):
        context = {"value": 1}
        return self.render_section(request, "counter", context)

    @dx_route("count/up/<int:value>", methods=["PUT"])
    def count_up(self, request, value):
        value += value
        context = {"value": value}
        if value < 100:
            return self.render_section(request, "counter", context)
        else:
            return self.render_section(request, "counter-exceeded", context)
