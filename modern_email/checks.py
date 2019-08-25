from django.core.checks import Info, Warning, register

from . import settings
from .static import static_exists


@register()
def check_logo_image(app_configs, **kwargs):
    errors = []

    if app_configs is None or "modern_email" in app_configs:
        if settings.LOGO_IMAGE is None:
            errors.append(
                Info(
                    "settings.MODERN_EMAIL_LOGO_IMAGE is not set. Your logo will not be shown in emails.",
                    id="modern_email.I001",
                )
            )
        else:
            if not static_exists(settings.LOGO_IMAGE):
                errors.append(
                    Warning(
                        "settings.MODERN_EMAIL_LOGO_IMAGE is invalid. Your logo may not appear in emails.",
                        id="modern_email.W001",
                    )
                )

    return errors
