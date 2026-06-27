from django.urls import path, include

from .actions.parameter import ParameterInlineActionRouter
from .actions.simple import SimpleInlineActionRouter
from .views import ShowcasesIndexView

app_name = "showcases"

urlpatterns = [
    path("", ShowcasesIndexView.as_view(), name="list"),
    path("simple/", include(SimpleInlineActionRouter.dx_router())),
    path("counter/", include(ParameterInlineActionRouter.dx_router())),
]
