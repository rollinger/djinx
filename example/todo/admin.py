from django.contrib import admin

from todo.models import TodoListItem


class TodoListItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(TodoListItem, TodoListItemAdmin)
