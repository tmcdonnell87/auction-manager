from django.contrib import admin
from .models import Lot, Wine, Item
import nested_admin

class WineInline(nested_admin.NestedTabularInline):
    model = Wine
    extra = 0

class ItemInline(nested_admin.NestedStackedInline):
    model = Item
    extra = 0
    inlines = [WineInline,]

class LotAdmin(nested_admin.NestedModelAdmin):
    list_display = ('lot', 'type', 'title')
    inlines = [
        ItemInline,
    ]

admin.site.register(Lot, LotAdmin)
