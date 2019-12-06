import logging

from django import template
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.urls import reverse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from admin_link.utils import get_admin_link_url

from ..models import Blurb

register = template.Library()

EMPTY_BLURB = '<a href="{}"><i class="fas fa-edit"></i> Enter initial content for <strong>{}</strong></a>'
EDIT_LINK = (
    ' <a href="{}" class="blurb-edit-link"><i class="fas fa-edit"></i> Edit {}</a>'
)


@register.simple_tag(takes_context=True)
def blurb(context, identifier, plain=False):
    # identifier should be in the form of '<page>:<name>'
    try:
        blurb = Blurb.objects.all().get(identifier=identifier)
        if blurb.plain != plain:
            blurb.plain = plain
            blurb.save()
            logging.warning(
                "Auto-correcting blurb type of {} to plain={}".format(
                    blurb.identifier, plain
                )
            )
    except ObjectDoesNotExist:
        blurb = Blurb.objects.create(identifier=identifier, content=None, plain=plain)

    user = context.request.user
    is_superuser = user and user.is_superuser
    admin_link = get_admin_link_url(context, blurb, "change")

    if blurb.content is None:
        if is_superuser:
            return mark_safe(EMPTY_BLURB.format(admin_link, identifier))
        else:
            return ""
    else:
        if blurb.plain:
            content = escape(blurb.content)
        else:
            content = mark_safe(blurb.content)
        if is_superuser:
            edit_link = mark_safe(EDIT_LINK.format(admin_link, identifier))
            content = format_html("{}{}".format(content, edit_link))
        return content
