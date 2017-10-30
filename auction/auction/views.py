import csv
from django.views.generic import TemplateView
from django.http import HttpResponse
#from wkhtmltopdf.views import PDFTemplateView

from .models import Lot

def lot_description(lot):
    description = lot.description

    for item in lot.item_set.all():
        description += '\n\n'
        description += (item.description + '\n')
        for wine in item.wine_set.all():
            description += '- ' + wine.full_desc + '\n'
    if lot.restrictions:
        description += '\n\n' + lot.restrictions
    return description


def LotBidPalListView(request, **kwargs):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bidpal.csv"'
    qs = Lot.objects \
        .filter(auction__id=kwargs.get('auction'))
    if 'lot' in request.GET:
        qs = qs.filter(lot__in=request.GET['lot'].split(','))
    else:
        qs = qs.filter(confirmed=True)
    lots = qs.order_by('lot_number', 'category')
    writer = csv.writer(response)
    writer.writerow(['Lot', 'Title', 'Category', 'Description', 'Value', 'Start Bid', 'Min Raise', 'Type', 'Tax'])
    for lot in lots:
        writer.writerow([
            lot.lot_number,
            lot.title,
            lot.get_category_display(),
            lot_description(lot),
            lot.FMV,
            lot.start_bid,
            lot.min_raise,
            lot.get_type_display(),
            lot.tax
        ])
    return response

