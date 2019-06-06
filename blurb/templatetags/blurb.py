from django import template
from django.conf import settings

from blurb.exceptions import BlurbNotFilledException
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ..models import Blurb

register = template.Library()


@register.simple_tag()
def blurb(identifier):
    # identifier should be in the form of '<page>:<name>'
    try:
        blurb = Blurb.objects.all().get(identifier=identifier)
    except ObjectDoesNotExist:
        blurb = Blurb.objects.create(identifier=identifier, content=None)

    empty_message = '[DEBUG] Fill in the blurb "{}" in the admin console'
    if blurb.content == None:
        if settings.DEBUG:
            return empty_message.format(identifier)
        else:
            raise BlurbNotFilledException(identifier)
    else:
        return blurb.content