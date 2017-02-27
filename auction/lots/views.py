from django.shortcuts import render
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import csv

from .models import Lot
# Create your views here.

class LotReceiptView(LoginRequiredMixin, DetailView):
    model = Lot
    template_name = 'lots/receipt.html'
