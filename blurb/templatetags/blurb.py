from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe

from blurb.exceptions import BlurbNotFilledException
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ..models import Blurb

register = template.Library()

EMPTY_BLURB = '[Empty Blurb "{}"] <a href="{}">Enter initial content as admin <i class="fas fa-edit"></i></a>'
EDIT_LINK = ' <a href="{}"><i class="fas fa-edit"></i></a>'


@register.simple_tag(takes_context=True)
def blurb(context, identifier):
    # identifier should be in the form of '<page>:<name>'
    try:
        blurb = Blurb.objects.all().get(identifier=identifier)
    except ObjectDoesNotExist:
        blurb = Blurb.objects.create(identifier=identifier, content=None)

    user = context.request.user
    is_superuser = user and user.is_superuser
    admin_link = reverse("admin:blurb_blurb_change", args=(blurb.id,))

    if blurb.content == None:
        if settings.DEBUG:
            empty_message = EMPTY_BLURB.format(identifier, admin_link)
            return mark_safe(empty_message)
        else:
            raise BlurbNotFilledException(identifier)
    else:
        content = blurb.content
        if is_superuser:
            content = blurb.content + EDIT_LINK.format(admin_link)
        return mark_safe(content)
