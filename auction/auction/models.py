from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class Lot(models.Model):
    LIVE = 'L'
    SILENT = 'S'
    type = models.CharField(
        choices=((LIVE, 'Live'), (SILENT, 'Silent')),
        default=SILENT,
        max_length=1,
    )
    lot = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=50)
    short_desc = models.CharField(
        blank=True,
        max_length=140,
        help_text='A short description for a slide or card'
    )
    description = models.TextField(
        blank=True,
        help_text='A long description suitable for printed text (e.g. website, program)'
    )
    restrictions = models.CharField(blank=True, max_length=140)
    FMV = models.PositiveIntegerField(null=True)
    predicted_sale = models.PositiveIntegerField(null=True)
    cost = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    start_bid = models.PositiveIntegerField(null=True)
    min_raise = models.PositiveIntegerField(null=True)
    complete = models.BooleanField(
        default=False,
        help_text='The lot description and items are complete based on donation form'
    )
    reviewed = models.BooleanField(
        default=False,
        help_text='The lot has been reviewed for accuracy by an auction chair'
    )
    received = models.BooleanField(
        default=False,
        help_text='The auction committee is in possession of all items in the lot'
    )
    confirmed = models.BooleanField(
        default=False,
        help_text='The items has been reviewed complete and available on-site for sale'
    )
    notes = models.TextField(
        blank=True,
        help_text='Internal notes on the lot'
    )
    item_description_override = models.TextField(
        blank=True,
        help_text='A text description of the items to override the default'
    )
    def image_thumbnail(self):
        return mark_safe('<img src="/uploads/%s" width="50" height="5-" />' % (self.image))
    image_thumbnail.short_description = 'Preview'
    image_thumbnail.allow_tags = True
    def __str__(self):
        return self.type + '-' + str(self.lot) + '-' + self.title

class Item(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=140)
    onsite_pickup = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=50)
    contact_point = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.description


class Wine(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50)
    size = models.CharField(default='750 ml', max_length=10)
    qty = models.PositiveSmallIntegerField(default=1)
    rating = models.CharField(blank=True, max_length=10)
    confirmed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.year) + ' ' + self.description + ' (' + self.size + ') x' + str(self.qty)
    @property
    def full_desc(self):
        return str(self.year) + ' ' + self.description + \
        (' (' + self.rating + ') - ' if self.rating else ' - ') + \
        self.size + ' (' + str(self.qty) + ')'

"""
class Auction(models.Model):
    default_contact_name = models.CharField(max_length=50)
    default_contact_point = models.CharField(max_length=50)
"""
