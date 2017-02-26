from django.db import models

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
    short_desc = models.CharField(
        blank=True,
        max_length=140,
        help_text='A short description for a slide or card'
    )
    description = models.TextField(
        blank=True,
        help_text='A long description suitable for printed text (e.g. website, program)'
    )
    title = models.CharField(max_length=50)
    restrictions = models.CharField(blank=True, max_length=140)
    FMV = models.PositiveIntegerField(null=True)
    predicted_sale = models.PositiveIntegerField(null=True)
    cost = models.PositiveIntegerField(null=True)
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

class Item(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    description = models.CharField(max_length=140)
    onsite_pickup = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=50)
    contact_point = models.CharField(max_length=50)

class Wine(models.Model):
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50)
    size = models.CharField(default='750 ml', max_length=10)
    qty = models.PositiveSmallIntegerField(default=1)
    rating = models.CharField(blank=True, max_length=10)


