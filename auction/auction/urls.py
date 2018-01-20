# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^(?P<auction_id>.+)/lots$',
        view=views.LotView.as_view(),
        name='lot-list'
    ),
    url(
        regex=r'^(?P<auction_id>.+)/bidpal$',
        view=views.LotBidPalListView,
        name='bidpal-csv'
    ),
    url(
        regex=r'^(?P<auction_id>.+)/receipts$',
        view=views.LotReceiptListView.as_view(),
        name="receipt-list",
    ),
    url(
        regex=r'^(?P<auction_id>.+)/silent$',
        view=views.LotSilentListView.as_view(),
        name="slide-list",
    ),
    url(
        regex=r'^(?P<auction_id>.+)/onsite$',
        view=views.OnSiteListView.as_view(),
        name="onsite-pickup-list",
    ),
]
