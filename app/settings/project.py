"""Add project specific settings here.

This way, you only need to update `base.py` when you fetch changes from
`django-template`. Settings that may change between different deployments
should be defined in .env.
"""
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
