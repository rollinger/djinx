from django.urls import path, include

from .actions.parameter import ParameterInlineActionRouter
from .actions.simple import SimpleInlineActionRouter
from .views import ShowcasesIndexView

app_name = "showcases"

urlpatterns = [
    path("", ShowcasesIndexView.as_view(), name="list"),
    path("simple/", include(SimpleInlineActionRouter.url_patterns())),
    path("counter/", include(ParameterInlineActionRouter.url_patterns())),
]
