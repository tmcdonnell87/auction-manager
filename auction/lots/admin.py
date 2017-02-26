from django.contrib import admin
from .models import Lot, Wine, Item

# Register your models here.
class WineInline(admin.TabularInline):
    model = Wine
    verbose_name_plural = 'Wines'
    min_num = 0

class ItemInline(admin.StackedInline):
    model = Item
    verbose_name_plural = 'Items'
    min_num = 0

@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ('lot', 'type', 'title')
    inlines = [
        ItemInline,
        WineInline,
    ]
