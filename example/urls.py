from django.urls import path
from django.views.generic import TemplateView

from .views import *

app_name = "example"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "blurb_test",
        TemplateView.as_view(template_name="example/blurb_test.html"),
        name="blurb-test",
    ),
    path(
        "carousel_test",
        TemplateView.as_view(template_name="example/carousel_test.html"),
        name="carousel-test",
    ),
]
