from django.urls import path
from django.views.generic import RedirectView, TemplateView

from modern_email.views import TestView

from . import views

app_name = "modern_email"
urlpatterns = [
    path("", RedirectView.as_view(url="test"), name="test"),
    path("test", TestView.as_view(), name="test"),
]
