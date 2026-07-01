from django.urls import path, include


from todo.views import TodoListDXBattery

app_name = "todo"

urlpatterns = [
    path("", include(TodoListDXBattery.url_patterns())),
]
