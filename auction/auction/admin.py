import math
from django.contrib import admin
from django.db import models
from django.forms import Textarea, ModelForm, SelectMultiple
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _

import nested_admin
from .models import (
    Lot,
    Wine,
    Item,
    Donation,
    DonationForm,
    Auction
)


class PrepopulatedRelatedFieldWidgetWrapper(admin.widgets.RelatedFieldWidgetWrapper):
    def __init__(self, widget, rel, admin_site, source, **kwargs):
        super(PrepopulatedRelatedFieldWidgetWrapper, self).__init__(widget, rel, admin_site, **kwargs)
        self.source = source

    def get_context(self, name, value, attrs):
        context = super(PrepopulatedRelatedFieldWidgetWrapper, self).get_context(name, value, attrs)
        url_params = (context['url_params'] + '&' + self.source) if context.get('url_params') else self.source
        context.update(url_params=url_params)
        return context


class DonationAdminForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['assigned_to_lots']

    def __init__(self, *args, **kwargs):
        super(DonationAdminForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to_lots'].widget = PrepopulatedRelatedFieldWidgetWrapper(
            admin.widgets.FilteredSelectMultiple(
                'Items',
                is_stacked=False,
            ),
            Donation._meta.get_field('assigned_to_lots').rel,
            self.admin_site,
            'from_donation={id}'.format(id=self.instance.id)
        )
        if hasattr(self.instance, 'auction'):
            self.fields['assigned_to_lots'].queryset = Lot.objects.filter(
                auction_id=self.instance.auction.id)


class ItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        lot_query = None
        if self.instance.donation:
            donation = self.instance.donation
            lots = [lot.id for lot in donation.assigned_to_lots.all()]
            if lots:
                lot_query = Lot.objects.filter(pk__in=lots)
            elif donation.auction:
                lot_query = Lot.objects.filter(auction_id=donation.auction.id)
            self.fields['lot'].queryset = lot_query
        if self.instance.lot:
            lot = self.instance.lot
            donations = [donation.id for donation in lot.donation_set.all()]
            if donations:
                donation_query = Donation.objects.filter(pk__in=donations)
            elif lot.auction:
                donation_query = Donation.objects.filter(auction_id=lot.auction.id)
            self.fields['donation'].queryset = donation_query


class WineInline(nested_admin.NestedTabularInline):
    model = Wine
    extra = 0

class LotItemInline(nested_admin.NestedStackedInline):
    model = Item
    extra = 0
    inlines = [WineInline,]


class DonationItemInline(nested_admin.NestedStackedInline):
    model = Item
    inlines = [WineInline,]
    extra = 0
    template = 'stacked_inline.html'
    form = ItemForm
    """
    formset = ItemFormset

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.args:
            return self.parent_model.objects.get(pk=resolved.args[0])
        return None

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(DonationItemInline, self).get_formset(request, obj, **kwargs)
        formset.donation = self.get_parent_object_from_request(request)
        return formset
    """

class DonationFormAdmin(admin.ModelAdmin):
    pass

class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'auction_actions',
    )
    list_display = ('name', 'date', 'auction_actions',)

class DonationAdmin(nested_admin.NestedModelAdmin):
    def __init__(self, model, admin_site):
        super(DonationAdmin,self).__init__(model, admin_site)
        self.form.admin_site = admin_site # capture the admin_site

    def associated_items(self, obj):
        return str(Item.objects.filter(donation_id=obj.id).count())

    def associated_lots(self, obj):
        return mark_safe(
            format_html_join(
                '\n', '<a href="{}" target="_blank">{}</a>',
                ((reverse('admin:auction_lot_change', args=[lot.id]), lot.lot_number) for lot in obj.assigned_to_lots.all())
            )
        )

    inlines = [
        DonationItemInline,
    ]
    list_display = (
        'auction',
        'category',
        'donor_organization',
        'donor_name',
        'donor_email',
        'donor_phone',
        'donor_address',
        'guardsmen_contact',
        'auction_value',
        'auction_items',
        'associated_items',
        'associated_lots',
        'complete',
        'active',
        'inactive_reason'
    )
    list_editable = ('category', 'complete',)
    list_filter = ('auction', 'active', 'category', 'complete', )
    readonly_fields = (
        'donation_actions',
    )
    fieldsets = (
        ('Main', {
            'fields': ('auction', 'source_form', 'form_entry_number', 'category')
        }),
        ('Donor', {
            'fields': ('donor_organization', 'donor_name', 'donor_email', 'donor_phone', 'donor_address', 'image_upload_link', 'image')
        }),
        ('Auction', {
            'fields': ('auction_items', 'auction_description', 'auction_value', 'auction_contact_point', 'delivery_method', 'special_instructions')
        }),
        ('Admin', {
            'fields': ('complete', 'active', 'inactive_reason')
        }),
        ('Other', {
            'fields': ('guardsmen_contact',)
        }),
        ('Actions', {
            'fields': ('assigned_to_lots', 'donation_actions',)
        }),
    )
    search_fields = ['donor_name', 'donor_organization', 'auction_items']
    form = DonationAdminForm


class LotAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        LotItemInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80})},
    }
    readonly_fields = (
        'generate_materials',
    )
    fieldsets = (
        ('Main', {
            'fields': ('auction', 'lot_number', 'title', 'type', 'category', )
        }),
        ('Description', {
            'fields': ('short_desc', 'description', 'restrictions', 'FMV', 'image', )
        }),
        ('Other Description', {
            'classes': ('collapse', ),
            'fields': ('pickup_instructions', 'item_description_override',)
        }),
        ('Bidding', {
            'fields': ('start_bid', 'min_raise',)
        }),

        ('Financial', {
            'fields': ('predicted_sale', 'acquisition_cost', 'actual_sale', 'tax_percentage', )
        }),
        ('Tracking', {
            'fields': ('complete', 'confirmed', 'pulled', 'extra', 'notes', )
        }),
        ('Actions', {
            'fields': ('generate_materials', )
        })
    )
    list_display = ('auction', 'lot_number', 'title', 'tax_percentage', 'type', 'category', 'FMV', 'start_bid', 'min_raise', 'complete', 'confirmed')
    list_filter = ('auction', 'type', 'category')
    search_fields = ['lot_number', 'title', 'short_desc']
    list_editable = ('lot_number', 'title', 'type', 'tax_percentage', 'category', 'FMV', 'start_bid', 'min_raise', 'complete', 'confirmed')
    ordering = ('lot_number', )

    def get_changeform_initial_data(self, request):
        def get_starting_bid(FMV):
            if not FMV:
                return 0
            base = FMV * 0.4
            if base < 100:
                return int(math.ceil(base / 10)) * 10
            if base < 200:
                return int(math.ceil(base / 20)) * 20
            if base < 500:
                return int(math.ceil(base / 50)) * 50
            else:
                return int(math.ceil(base / 50)) * 50
        def get_min_raise(FMV):
            if not FMV:
                return 0
            base = FMV * 0.1
            if base < 200:
                return 10
            if base < 200:
                return 20
            if base < 500:
                return 50
            else:
                return 100

        if request.GET.get('from_donation'):
            donation_id = request.GET['from_donation']
            donation = Donation.objects.get(pk=donation_id)
            category = donation.category[0] if not donation.auction_value or donation.auction_value < 1200 else 'X'
            lot_number = None
            try:
                lot_number = Lot.objects.filter(category=category, auction_id=donation.auction.id).latest('lot_number').lot_number + 1
                if Lot.objects.get(lot_number=lot_number, auction_id=donation.auction.id):
                    lot_number = None
                    raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                if not lot_number:
                    try:
                        lot_number = Lot.objects.filter(auction=donation.auction).latest('lot_number').lot_number + 1
                    except ObjectDoesNotExist:
                        lot_number = 101
            initial_data = {
                'auction': donation.auction,
                'lot_number': lot_number,
                'category': category,
                'title': donation.donor_organization,
                'description': donation.auction_description,
                'image': donation.image,
                'short_desc': donation.auction_items,
                'FMV': donation.auction_value,
                'start_bid': get_starting_bid(donation.auction_value),
                'min_raise': get_min_raise(donation.auction_value),
                'notes': donation.special_instructions,
                'auction_contact_point': donation.auction_contact_point or donation.auction.auction_primary.name,
            }
        else:
            initial_data = super().get_changeform_initial_data(request)
        return initial_data

class WineAdmin(admin.ModelAdmin):
    list_display = ('item', 'year', 'description', 'size', 'qty', 'rating', 'confirmed')
    search_fields = ('year', 'description', 'item__title', 'lot__title')
    list_editable = ('year', 'description', 'size', 'qty', 'rating', 'confirmed')


class ItemAuctionListFilter(admin.SimpleListFilter):
    title = _('Auction')
    parameter_name = 'auction'
    def lookups(self, request, model_admin):
        return [(a.id, a) for a in Auction.objects.all()]
    def queryset(self, request, queryset):
        # hacky
        ids = [i.id for i in queryset if str(i.auction().id) == self.value()]
        return queryset.filter(id__in=ids)
        #return [i for i in queryset.all()]

class ItemAdmin(nested_admin.NestedModelAdmin):
    readonly_fields = ('auction',)
    list_display = (
        'auction',
        'donation',
        'lot',
        'description',
        'onsite_pickup',
        'contact_name',
        'contact_point',
        'location',
        'location_notes',
        'item_notes',
    )
    search_fields = ('lot__title', 'description')
    list_editable = (
        'description',
        'onsite_pickup',
        'contact_name',
        'contact_point',
        'location',
        'location_notes',
    )
    list_filter = ('location', ItemAuctionListFilter,)
    inlines = [
        WineInline
    ]
    def get_changeform_initial_data(self, request):

        if request.GET.get('from_donation'):
            donation_id = request.GET['from_donation']
            donation = Donation.objects.get(pk=donation_id)
            # location
            location = None
            if donation.delivery_method:
                if 'SF Wine Center' in donation.delivery_method:
                    location = 'SFWC'
                elif 'Guardsmen Office' in donation.delivery_method:
                    location = 'OFFICE'
            if not location:
                location = 'OTHER'
            # contact point
            if donation.auction_contact_point:
                contact_point = donation.auction_contact_point
                contact_name = None
            else:
                contact_point = donation.auction.contact_email
                contact_name = donation.auction.auction_primary.name
            try:
                lot = donation.assigned_to_lots.all()[0]
            except:
                lot = None
            initial_data = {
                'donation': donation,
                'lot': lot,
                'description': donation.auction_items,
                'contact_name': contact_name,
                'contact_point': contact_point,
                'location': location,
                'item_notes': donation.special_instructions,
            }
        else:
            initial_data = super().get_changeform_initial_data(request)
        return initial_data


admin.site.register(Lot, LotAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(DonationForm, DonationFormAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Auction, AuctionAdmin)
