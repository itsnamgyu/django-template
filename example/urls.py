from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "example"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "blurb_test",
        TemplateView.as_view(template_name="example/blurb_test.html"),
        name="blurb_test",
    ),
    path(
        "carousel_test",
        TemplateView.as_view(template_name="example/carousel_test.html"),
        name="carousel_test",
    ),
]
