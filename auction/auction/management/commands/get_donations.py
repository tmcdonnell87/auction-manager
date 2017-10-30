import datetime
import os
from pytz import timezone
from django.core.management.base import BaseCommand
from django.conf import settings
from pyfoo import PyfooAPI

from ...models import (
    Auction,
    DonationForm,
    Donation
)
class Command(BaseCommand):
    help = "Get donations from Wufoo."

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action="store_true")

    def handle(self, *_, **options):
        auctions = Auction.objects.filter(
            date__gt=datetime.date.today(),
            donation_form__isnull=False,
            donation_form__hash__isnull=False
        )
        api = PyfooAPI('guardsmen', settings.WUFOO_API_KEY)
        localtz = timezone(settings.TIME_ZONE)
        for auction in auctions:
            donation_form = auction.donation_form
            try:
                wufoo_form = next(x for x in api.forms if x.Hash == donation_form.hash)
            except StopIteration:
                continue
            entries = wufoo_form.get_entries(page_size=wufoo_form.entry_count)
            entries = [x for x in entries if x['CompleteSubmission']]
            processed = Donation.objects.filter(
                source_form__id=donation_form.id
            )
            for entry in entries:
                try:
                    donation = next(x for x in processed if x.form_entry_number == int(entry['EntryId']))
                    if not options['overwrite']:
                        continue
                except StopIteration:
                    donation = Donation(
                        auction=auction,
                        source_form=donation_form,
                        form_entry_number=entry['EntryId'],
                    )
                # get info from form
                donor_organization = entry['Field1']
                donor_name = entry['Field2'] + ' ' + entry['Field3']
                donor_email = entry['Field11']
                donor_address = entry['Field4'] + os.linesep + \
                    ((entry['Field5'] + os.linesep) if entry['Field5'] else '') +\
                    entry['Field6'] + ', ' + entry['Field7'] + ' ' + entry['Field8'] + os.linesep +\
                    entry['Field9']
                guardsmen_contact = (entry['Field13'] + ' ' + entry['Field14']).strip()
                auction_items = entry['Field224']
                auction_value = entry['Field438']
                special_instructions = entry['Field327']
                delivery_method = entry['Field326']
                form_created_time = None
                if entry['DateCreated']:
                    form_created_time = localtz.localize(datetime.datetime.strptime(
                        entry['DateCreated'],
                        '%Y-%m-%d %H:%M:%S'
                    ))
                form_updated_time = None
                if entry['DateUpdated']:
                    form_updated_time = localtz.localize(datetime.datetime.strptime(
                        entry['DateUpdated'],
                        '%Y-%m-%d %H:%M:%S'
                    ))
                donor_phone = None
                if donation_form.phone_number_field:
                    donor_phone = entry['Field{}'.format(donation_form.phone_number_field)]
                auction_description = None
                if donation_form.item_description_field:
                    auction_description = entry['Field{}'.format(donation_form.item_description_field)]
                auction_contact_point = None
                if donation_form.auction_provide_contact_field:
                    auction_contact_type = entry['Field{}'.format(donation_form.auction_provide_contact_field)]
                    if 'above' in auction_contact_type:
                        auction_contact_point = donor_name + ' (' + donor_email + ')'
                    elif donation_form.auction_contact_point_field and entry['Field{}'.format(donation_form.auction_contact_point_field)]:
                        auction_contact_point = entry['Field{}'.format(donation_form.auction_contact_point_field)]
                donation.donor_organization = donor_organization
                donation.donor_name = donor_name
                donation.donor_email = donor_email
                donation.donor_address = donor_address
                donation.guardsmen_contact = guardsmen_contact
                donation.auction_items = auction_items
                donation.auction_value = auction_value
                donation.special_instructions = special_instructions
                donation.delivery_method = delivery_method
                donation.donor_phone = donor_phone
                donation.auction_description = auction_description
                donation.auction_contact_point = auction_contact_point
                donation.form_created_time = form_created_time
                donation.form_updated_time = form_updated_time
                donation.save()
