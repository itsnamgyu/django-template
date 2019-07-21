from django.conf import settings

TEST_PUBLIC_KEY: str = getattr(settings, STRIPE_TEST_PUBLIC_KEY, None)
TEST_SECRET_KEY: str = getattr(settings, STRIPE_TEST_SECRET_KEY, None)
LIVE_PUBLIC_KEY: str = getattr(settings, STRIPE_LIVE_PUBLIC_KEY, None)
LIVE_SECRET_KEY: str = getattr(settings, STRIPE_LIVE_SECRET_KEY, None)

SUPPORT_EMAIL: str = getattr(settings, STRIPE_SUPPORT_EMAIL, None)
