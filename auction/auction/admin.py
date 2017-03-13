from django.contrib import admin
from django.db import models
from django.forms import Textarea
import nested_admin
from .models import Lot, Wine, Item


class WineInline(nested_admin.NestedTabularInline):
    model = Wine
    extra = 0

class ItemInline(nested_admin.NestedStackedInline):
    model = Item
    extra = 0
    inlines = [WineInline,]

class LotAdmin(nested_admin.NestedModelAdmin):
    list_display = ('lot', 'type', 'title', 'FMV', 'reviewed', 'received', 'confirmed')
    inlines = [
        ItemInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'cols': 80})},
    }
    fieldsets = (
        ('Main', {
            'fields': ('type', 'lot', 'title',)
        }),
        ('Description', {
            'fields': ('short_desc', 'description', 'restrictions', 'image')
        }),
        ('Advanced', {
            'classes': ('collapse', ),
            'fields': ('item_description_override',)
        }),
        ('Financial', {
            'fields': ('FMV', 'predicted_sale', 'cost', 'start_bid', 'min_raise',)
        }),
        ('Review', {
            'fields': ('reviewed', 'received', 'confirmed',)
        }),
        ('Admin', {
            'fields': ('notes',)
        }),
    )
    list_filter = ('type', )
    search_fields = ['title', 'short_desc']

class WineAdmin(admin.ModelAdmin):
    list_display = ('item', 'year', 'description', 'size', 'qty', 'rating', 'confirmed')
    search_fields = ('year', 'description')
    list_editable = ('year', 'description', 'size', 'qty', 'rating', 'confirmed')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('lot', 'description', 'onsite_pickup', 'contact_name', 'contact_point', 'confirmed')
    search_fields = ('lot__title', 'description')
    list_editable = ('description', 'onsite_pickup', 'contact_name', 'contact_point', 'confirmed')

admin.site.register(Lot, LotAdmin)
admin.site.register(Wine, WineAdmin)
admin.site.register(Item, ItemAdmin)
