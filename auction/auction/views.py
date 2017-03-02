import csv
from django.views.generic import TemplateView
from django.http import HttpResponse
from wkhtmltopdf.views import PDFTemplateView

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


# Create your views here.
class LotReceiptListView(TemplateView):
    template_name = 'lots/receipt.html'
    def lots(self):
        return Lot.objects.all()

class LotReceiptPDFView(PDFTemplateView, LotReceiptListView):
    template_name = 'lots/receipt.html'
    filename = None

class LotSlideListView(TemplateView):
    template_name = 'lots/live_slide.html'
    def lots(self):
        return Lot.objects.all()

def LotBidPalListView(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bidpal.csv"'
    lots = Lot.objects.all()
    writer = csv.writer(response)
    writer.writerow(['Lot', 'Title', 'Category', 'Description', 'Value', 'Start Bid', 'Min Raise', 'Type'])
    for lot in lots:
        writer.writerow([lot.lot, lot.title, '', lot_description(lot), lot.FMV, lot.start_bid, lot.min_raise, lot.get_type_display()])
    return response

class LotSlidePDFView(PDFTemplateView, LotSlideListView):
    template_name = 'lots/live_slide.html'
    cmd_options = {
        'javascript-delay': 500,
        'margin-top': 0,
        'margin-left': 0,
        'margin-right': 0,
        'margin-bottom': 0,
        'page-width': '13.33in',
        'page-height': '7.5in',
        'print-media-type': True,
    }
    filename=None
