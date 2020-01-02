import random

from django.apps import apps
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "example/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dt_content"] = apps.is_installed("dt_content")
        context["dt_stripe"] = apps.is_installed("dt_stripe")
        context["simple_sendgrid"] = apps.is_installed("simple_sendgrid")
        return context


class CarouselTestView(TemplateView):
    template_name = "example/carousel_test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel"] = random.randrange(1, 100)
        return context
