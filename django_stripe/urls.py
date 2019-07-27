from django.urls import path

from django_stripe import views
from django_stripe.views import checkout_completed_webhook

app_name = 'django_stripe'
urlpatterns = [
    path('webhook/checkout-completed', views.checkout_completed_webhook,
         'webhook_checkout_completed'),
    path('checkout-success', views.checkout_success, 'checkout_success'),
]
