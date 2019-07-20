from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def _is_absolute(url):
    return bool(urlparse(url).netloc)


STATIC_URL = getattr(settings, 'STATIC_URL', None)
ABSOLUTE_STATIC_URL: bool = STATIC_URL and _is_absolute(STATIC_URL)

STATIC_HOST: str = getattr(settings, 'MODERN_EMAIL_STATIC_HOST', None)
if not ABSOLUTE_STATIC_URL and not STATIC_HOST:
    raise ImproperlyConfigured(
        'MODERN_EMAIL_STATIC_HOST was must be provided when STATIC_URL is not absolute'
    )

LOGO_IMAGE: str = getattr(settings, 'MODERN_EMAIL_LOGO_IMAGE', None)
LOGO_MAX_LENGTH: str = getattr(settings, 'MODERN_EMAIL_LOGO_MAX_LENGTH', 100)

ORGANIZATION_NAME = getattr(settings, 'MODERN_EMAIL_ORGANIZATION_NAME', None)
ADDRESS_LINE_1 = getattr(settings, 'MODERN_EMAIL_ADDRESS_LINE_1', None)
ADDRESS_LINE_2 = getattr(settings, 'MODERN_EMAIL_ADDRESS_LINE_2', None)
SUPPORT_EMAIL = getattr(settings, 'MODERN_EMAIL_SUPPORT_EMAIL', None)
COPYRIGHT_START_YEAR = getattr(settings, 'MODERN_EMAIL_COPYRIGHT_START_YEAR',
                               None)
