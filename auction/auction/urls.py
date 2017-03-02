# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^receipts$',
        view=views.LotReceiptListView.as_view(),
        name='receipt-list'
    ),
    url(
        regex=r'^pdf/receipts$',
        view=views.LotReceiptPDFView.as_view(),
        name='receipt-pdf'
    ),
    url(
        regex=r'^slides$',
        view=views.LotSlideListView.as_view(),
        name='slide-list'
    ),
    url(
        regex=r'^pdf/slides$',
        view=views.LotSlidePDFView.as_view(),
        name='slide-pdf'
    ),
    url(
        regex=r'^bidpal$',
        view=views.LotBidPalListView,
        name='bidpal-csv'
    ),

]
