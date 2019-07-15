from urllib import parse

from django.contrib.staticfiles import finders
from django.templatetags.static import static

from . import settings


def static_exists(path):
    system_path = finders.find(path)
    return system_path is not None


def static_absolute(path):
    static_path = static(path)
    if settings.ABSOLUTE_STATIC_URL:
        return static_path
    else:
        return parse.urljoin(settings.STATIC_HOST, static_path)
