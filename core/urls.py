from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

]
