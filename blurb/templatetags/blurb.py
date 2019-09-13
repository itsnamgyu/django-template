from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from admin_link.utils import get_admin_link_url

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
    admin_link = get_admin_link_url(context, blurb, "change")

    if blurb.content is None:
        if is_superuser or settings.DEBUG:
            return mark_safe(EMPTY_BLURB.format(identifier, admin_link))
        else:
            return ""
    else:
        content = blurb.content
        if is_superuser:
            content = content + EDIT_LINK.format(admin_link)
        return mark_safe(content)
