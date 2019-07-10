from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'example'
urlpatterns = [
    path('',
         TemplateView.as_view(template_name='example/index.html'),
         name='index'),
]