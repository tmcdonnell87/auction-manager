from django.apps import AppConfig


class LotsConfig(AppConfig):
    name = 'auction.lots'
    verbose_name = "Lots"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
