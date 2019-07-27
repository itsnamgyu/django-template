import datetime

from django import template

from modern_email.static import static_absolute as get_static_absolute_path
from modern_email import settings

register = template.Library()


@register.simple_tag
def static_absolute(path):
    return get_static_absolute_path(path)


@register.simple_tag
def static_logo():
    return static_absolute(settings.LOGO_IMAGE)
