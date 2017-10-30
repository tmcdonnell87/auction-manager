from django.contrib import admin
from django.db import models
from django.forms import Textarea
#from django.utils.html import format_html
#from django.core.urlresolvers import reverse
import nested_admin
from .models import (
    Lot,
    Wine,
    Item,
    Donation,
    DonationForm,
    Auction
)

class WineInline(nested_admin.NestedTabularInline):
    model = Wine
    extra = 0

class ItemInline(nested_admin.NestedStackedInline):
    model = Item
    extra = 0
    inlines = [WineInline,]

class DonationFormAdmin(admin.ModelAdmin):
    pass

class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = (
        'auction_actions',
    )
    list_display = ('name', 'date', 'auction_actions',)

class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'auction',
        'donor_organization',
        'donor_name',
        'donor_email',
        'donor_phone',
        'donor_address',
        'guardsmen_contact',
        'auction_value',
        'auction_items',
        'active',
        'inactive_reason'
    )
    list_filter = ('auction', 'active')
    inlines = (ItemInline, )
    fieldsets = (
        ('Main',{
            'fields': ('auction', 'source_form', 'form_entry_number')
        }),
        ('Donor', {
            'fields': ('donor_organization', 'donor_name', 'donor_email', 'donor_phone', 'donor_address')
        }),
        ('Auction', {
            'fields': ('auction_items', 'auction_description', 'auction_value', 'auction_contact_point', 'delivery_method', 'special_instructions')
        }),
        ('Admin', {
            'fields': ('active', 'inactive_reason')
        }),
        ('Other', {
            'fields': ('guardsmen_contact',)
        }),
    )
    search_fields = ['donor_name', 'donor_organization', 'auction_items']

class LotAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ItemInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80})},
    }
    fieldsets = (
        ('Main', {
            'fields': ('auction', 'lot_number', 'title', 'type', 'category', )
        }),
        ('Description', {
            'fields': ('short_desc', 'description', 'restrictions', 'image', 'FMV')
        }),
        ('Other Description', {
            'classes': ('collapse', ),
            'fields': ('pickup_instructions', 'item_description_override',)
        }),
        ('Bidding', {
            'fields': ('start_bid', 'min_raise',)
        }),

        ('Financial', {
            'fields': ('predicted_sale', 'acquisition_cost', 'actual_sale', 'tax_percentage')
        }),
        ('Tracking', {
            'fields': ('complete', 'confirmed', 'notes')
        }),
    )
    list_display = ('auction', 'lot_number', 'title', 'type', 'category', 'FMV')
    list_filter = ('auction', 'type', 'category')
    search_fields = ['lot_number', 'title', 'short_desc']
    list_editable = ('lot_number', 'title', 'type', 'category', 'FMV')
    ordering = ('lot_number', )

class WineAdmin(admin.ModelAdmin):
    list_display = ('item', 'year', 'description', 'size', 'qty', 'rating', 'confirmed')
    search_fields = ('year', 'description', 'item__title', 'lot__title')
    list_editable = ('year', 'description', 'size', 'qty', 'rating', 'confirmed')

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'lot',
        'description',
        'donation',
        'onsite_pickup',
        'contact_name',
        'contact_point',
        'location',
        'location_notes'
    )
    search_fields = ('lot__title', 'description')
    list_editable = (
        'description',
        'donation',
        'onsite_pickup',
        'contact_name',
        'contact_point',
        'location',
        'location_notes'
    )

admin.site.register(Lot, LotAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(DonationForm, DonationFormAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(Auction, AuctionAdmin)
