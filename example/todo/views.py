from djxi import DXEndpointBattery, dx_action
from djxi.router import dx_put, dx_post, dx_get, dx_delete

from todo.models import TodoListItem

INLINE_TEMPLATE = """
<dx-section name="todo-list">
    <div id="todo-list_container">
        <h3>TODO</h3>
        <input type="search" name="search" value={{search}} autofocus
           hx-post='{% url "todo:list" %}'
           hx-trigger="input changed delay:200ms, keyup[key=='Enter']"
           hx-target="#todo-list_container">
        <ul id="todo-list">
            {% for item in todo_items %}
                {#% dx_include "todo-item" %#}
                <li hx-get='{% url "todo:item" item.id %}' hx-trigger="load" hx-swap="outerHTML"></li>
            {% endfor %}
        </ul>
    </div>
</dx-section>

<dx-section name="todo-item">
    <li id="todo_item_{{item.id}}" 
    hx-get='{% url "todo:item-detail" item.id %}' hx-trigger="mouseenter delay:50ms" hx-swap="outerHTML">
        <div style="width: 250px;">
            {% if item.completed %}✅{% else %}❌{% endif %}
            {{ item.id }}: <b>{{ item.title }}</b>
        </div>
    </li>
</dx-section>

<dx-section name="todo-item-detail">
    <li id="todo_item_{{item.id}}"
    hx-get='{% url "todo:item" item.id %}' hx-trigger="mouseleave delay:50ms" hx-swap="outerHTML">
        <small><b>{{ item.title }}</b></small><br>
        {{ item.description }}
        {% if item.completed %}
            <a href="">Re open</a>
        {% else %}
            <a href="">Set complete</a>
        {% endif %}
        | <a href="">Edit</a> | <a href="">Delete</a>
    </li>
</dx-section>
"""


class TodoListDXBattery(DXEndpointBattery):
    section_inline = INLINE_TEMPLATE

    @dx_action("todo-list", methods=["GET", "POST"], name="list")
    def list(self, request):
        context = {}
        items = TodoListItem.objects.all()
        if request.method == "POST":
            search = getattr(request.POST, "search", None)
            if search:
                items = items.filter(title__icontains=search)
                context["search"] = search
        context = {"todo_items": items}
        return self.render_section(request, section_name="todo-list", context=context)

    @dx_action("todo-list/<int:item_id>", methods=["GET"], name="item")
    @dx_action("todo-list/<int:item_id>/detail", methods=["GET"], name="item-detail")
    def item(self, request, item_id):
        context = {"item": TodoListItem.objects.get(id=item_id)}
        if request.resolver_match.url_name == "item":
            return self.render_section(
                request, section_name="todo-item", context=context
            )
        elif request.resolver_match.url_name == "item-detail":
            return self.render_section(
                request, section_name="todo-item-detail", context=context
            )

    @dx_get("todo-list/<int:item_id>/edit", name="edit")
    @dx_put("todo-list/<int:item_id>/edit", name="edit")
    def update(self, request, item_id):
        pass

    @dx_get("todo-list/create", name="create")
    @dx_post("todo-list/create", name="create")
    def create(self, request, item_id):
        pass

    @dx_delete("todo-list/<int:item_id>/edit", name="delete")
    def delete(self, request, item_id):
        pass
