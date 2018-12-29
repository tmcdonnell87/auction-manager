from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class AuctionConfig(AppConfig):
    name = 'auction.auction'
    verbose_name = "Auction"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
