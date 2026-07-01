from django.apps import AppConfig


class TodoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todo"
    verbose_name = "Todo"

    def ready(self):
        pass
