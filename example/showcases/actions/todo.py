from djxi import DXEndpointBattery, dx_action

INLINE_TEMPLATE = """
<dx-section name="todo-list">
    <div hx-get={% url "load-todo-list" %} hx-trigger="load delay:100ms">
        <h3>TODO</h3>
        <ul id="todo-list"></ul>
        <div id="todo-add"></div>
    </div>
</dx-section>

<dx-section name="todo-item">
    {% for item in list %}
        <li>Item to do</li>
    {% empty %}
        <li>Nothing to do!</li>
    {% endfor %}
</dx-section>
"""


class SimpleInlineActionRouter(DXEndpointBattery):
    inline_template = INLINE_TEMPLATE

    @dx_action("todo-list/load", methods=["GET"])
    def load_todo_list(self, request):
        context = {"name": "Phil"}
        return self.render_section(
            request, section_name="confirm-button", context=context
        )
