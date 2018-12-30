from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem

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
    menu = (
        ParentItem('Auction', children=[
            ChildItem(model='auction.donation'),
            ChildItem(model='auction.lot'),
        ]),
    )
