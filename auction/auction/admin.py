from django.contrib import admin
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

admin.site.register(Lot, LotAdmin)
