from django.apps import AppConfig


class ModernEmailConfig(AppConfig):
    name = "modern_email"

    def ready(self):
        import modern_email.checks
