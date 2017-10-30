from django.apps import AppConfig


class AuctionConfig(AppConfig):
    name = 'auction.auction'
    verbose_name = "Auction"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
