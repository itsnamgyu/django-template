from django.urls import path
from django.views.generic import TemplateView

from modern_email.views import TestView

from . import views

app_name = "modern_email"
urlpatterns = [path("test", TestView.as_view(), name="test")]
