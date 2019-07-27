from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'base'
urlpatterns = [
    path('preview',
         TemplateView.as_view(template_name='base/preview.html'),
         name='preview'),
]
