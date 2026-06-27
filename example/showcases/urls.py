from django.urls import path, include
from django.views.generic import TemplateView

from .actions.parameter import ParameterInlineActionRouter
from .actions.simple import SimpleInlineActionRouter

app_name = "showcases"

urlpatterns = [
    path("", TemplateView.as_view(template_name="showcases/list.html"), name="list"),
    path("simple/", include(SimpleInlineActionRouter.dx_router())),
    path("counter/", include(ParameterInlineActionRouter.dx_router())),
]
