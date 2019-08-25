from django.shortcuts import render
from django.views.generic import TemplateView


class CarouselTestView(TemplateView):
    template_name = "example/carousel_test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel"] = random.randrange(1, 100)
        return context
