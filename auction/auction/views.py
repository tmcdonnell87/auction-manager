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
        qs = Lot.objects
        if 'lot' in self.request.GET:
            qs = qs.filter(lot__in=self.request.GET['lot'].split(','))
        else:
            qs = qs.all()
        qs = qs.filter(lot__lt=1000)
        qs = qs.order_by('lot')
        return qs

class LotSlideListView(TemplateView):
    template_name = 'lots/live_slide.html'
    def lots(self):
        qs = Lot.objects
        if 'lot' in self.request.GET:
            qs = qs.filter(lot__in=self.request.GET['lot'].split(','))
        else:
            qs = qs.filter(type='L')
        qs = qs.order_by('lot')
        return qs

class LotSilentListView(TemplateView):
    template_name = 'lots/silent.html'
    def lots(self):
        qs = Lot.objects
        if 'lot' in self.request.GET:
            qs = qs.filter(lot__in=self.request.GET['lot'].split(','))
        else:
            qs = qs.filter(type='S')
        qs = qs.filter(lot__lt=1000)
        qs = qs.order_by('lot')
        return qs

class LotOnsiteItemsListView(TemplateView):
    template_name = 'lots/onsite_items.html'
    def lots(self):
        qs = Lot.objects
        if 'lot' in self.request.GET:
            qs = qs.filter(lot__in=self.request.GET['lot'].split(','))
        else:
            qs = qs.all()
        qs = qs.filter(lot__lt=1000)
        qs = qs.order_by('lot')
        return qs

class LotPreviewEmailView(TemplateView):
    template_name = 'lots/preview_email.html'
    def lots(self):
        return Lot.objects.filter(type='L').order_by('lot')

class LotReceiptPDFView(PDFTemplateView, LotReceiptListView):
    template_name = 'lots/receipt.html'
    cmd_options = {
        'disable-smart-shrinking': True,
        'page-size': 'Letter',
        'disable-javascript': True
    }
    filename = None

class LotPreviewEmailPDFView(PDFTemplateView, LotPreviewEmailView):
    template_name = 'lots/preview_email.html'
    filename = None
    cmd_options = {
        'margin-top': 0,
        'margin-left': 0,
        'margin-right': 0,
        'margin-bottom': 0,
        'page-height': '11in',
        'page-width': '8.5in',
    }

class LotSlidePDFView(PDFTemplateView, LotSlideListView):
    template_name = 'lots/live_slide.html'
    cmd_options = {
        'javascript-delay': 500,
        'margin-top': 0,
        'margin-left': 0,
        'margin-right': 0,
        'margin-bottom': 0,
        'quiet': None,
        'page-width': '13.33in',
        'page-height': '7.5in',
        'print-media-type': True,
    }
    filename = None

def LotBidPalListView(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bidpal.csv"'
    qs = Lot.objects
    if 'lot' in request.GET:
        qs = qs.filter(lot__in=request.GET['lot'].split(','))
    else:
        qs = qs.all()
    qs = qs.filter(lot__lt=1000)
    lots = qs.order_by('lot', 'category')
    writer = csv.writer(response)
    writer.writerow(['Lot', 'Title', 'Category', 'Description', 'Value', 'Start Bid', 'Min Raise', 'Type'])
    for lot in lots:
        writer.writerow([
            lot.lot,
            lot.title,
            lot.get_category_display(),
            lot_description(lot),
            lot.FMV,
            lot.start_bid,
            lot.min_raise,
            lot.get_type_display()
        ])
    return response

