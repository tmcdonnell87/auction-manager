# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import path

from . import views

app_name = 'auction'
urlpatterns = [
    path(
        '<int:auction_id>/lots',
        views.LotView.as_view(),
        name='lot-list'
    ),
    path(
        '<int:auction_id>/bidpal',
        views.LotBidPalListView,
        name='bidpal-csv'
    ),
    path(
        '<int:auction_id>/receipts',
        views.LotReceiptListView.as_view(),
        name="receipt-list",
    ),
    path(
        '<int:auction_id>/silent',
        views.LotSilentListView.as_view(),
        name="slide-list",
    ),
    path(
        '<int:auction_id>/onsite',
        views.OnSiteListView.as_view(),
        name="onsite-pickup-list",
    ),
]
