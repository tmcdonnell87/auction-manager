# Generated by Django 2.1.4 on 2018-12-30 09:02

from django.db import migrations, models
from auction.auction.models import DONATION_TYPES

def forwads_func(apps, schema_editor):
    Donation = apps.get_model("auction", "Donation")
    db_alias = schema_editor.connection.alias
    new_categories = [t[0] for t in DONATION_TYPES]
    donations = Donation.objects.using(db_alias).all()
    for d in donations:
        dtype = d.category
        if dtype:
            normalized_type = dtype[0]
            d.category = normalized_type if normalized_type in new_categories else 'O'
            d.save()

def reverse_func(_, __):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0020_lot_extra'),
    ]

    operations = [
        migrations.RunPython(forwads_func, reverse_func),
        migrations.AlterField(
            model_name='donation',
            name='category',
            field=models.CharField(blank=True, choices=[('O', 'Other'), ('W', 'Wine'), ('G', 'Golf'), ('S', 'Sports'), ('E', 'Experiences'), ('R', 'Restaurants')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='form_entry_number',
            field=models.PositiveIntegerField(blank=True, help_text='The entry number of the donation form', null=True),
        ),
    ]
