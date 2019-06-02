from django.urls import path
from . import views

app_name = 'base'
urlpatterns = [
    path('preview', views.preview, name='preview'),
]