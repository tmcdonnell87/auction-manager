from django.db import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.core.urlresolvers import reverse

class DonationForm(models.Model):
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=32)
    phone_number_field = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='The Wufoo field ID for this data item'
    )
    logo_field = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='The Wufoo field ID for this data item'
    )
    item_description_field = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='The Wufoo field ID for this data item'
    )
    auction_provide_contact_field = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='The Wufoo field ID for this data item'
    )
    auction_contact_point_field = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text='The Wufoo field ID for this data item'
    )

    def __str__(self):
        return self.name

class Auction(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbr = models.CharField(
        max_length=16,
        unique=True,
        help_text='Abbreviation for use in application'
    )
    date = models.DateField()
    contact_email = models.EmailField(max_length=255)
    main_image = models.ImageField(null=True, blank=True)
    donation_form = models.ForeignKey(
        DonationForm,
        null=True,
        blank=True,
        help_text='The donation form associated with the auction'
    )
    chairmen = models.ManyToManyField(
        'users.User',
        related_name='events'
    )
    auction_primary = models.ForeignKey(
        'users.User',
        null=True,
        related_name='+',
        help_text='Person to list on the auction receipt as follow-up contact for any issues'
    )
    def auction_actions(self):
        return mark_safe(
            format_html(
                '<a class="btn" href="{}" target="_blank">Generate BidPal</a>&nbsp;'
                '<a class="btn" href="{}" target="_blank">Generate Displays (not built)</a>&nbsp;'
                '<a class="btn" href="{}" target="_blank">Generate Receipts (not built)</a>&nbsp;',
                reverse('auction:bidpal-csv', args=[self.id]),
                reverse('admin:index'),
                reverse('admin:index')
            )
        )
    auction_actions.short_description = 'Auction Actions'
    auction_actions.allow_tags = True

    def __str__(self):
        return self.abbr

class Lot(models.Model):
    auction = models.ForeignKey(
        Auction,
        help_text='The auction this lot is associated with'
    )
    lot_number = models.PositiveSmallIntegerField(unique=True, db_index=True)
    # Categories
    LIVE = 'L'
    SILENT = 'S'
    type = models.CharField(
        choices=((LIVE, 'Live'), (SILENT, 'Silent')),
        default=SILENT,
        max_length=1,
    )
    WINE = 'W'
    GOLF = 'G'
    EXPERIENCE = 'E'
    OTHER = 'O'
    SUPERSILENT = 'S'
    category = models.CharField(
        choices=(
            (WINE, 'Wine'),
            (GOLF, 'Golf'),
            (EXPERIENCE, 'Experiences'),
            (OTHER, 'Other'),
            (SUPERSILENT, 'Super Silent')
        ),
        default=OTHER,
        max_length=1
    )
    # title and program
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
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    FMV = models.PositiveIntegerField(null=True)
    pickup_instructions = models.TextField(
        blank=True,
        help_text='Additional redemption instructions for the lot'
    )
    item_description_override = models.TextField(
        blank=True,
        help_text='A HTML-enabled description of the items to override the default rendering'
    )

    # bidding
    start_bid = models.PositiveIntegerField(null=True)
    min_raise = models.PositiveIntegerField(null=True)

    # cost basis tracking
    predicted_sale = models.PositiveIntegerField(null=True, blank=True)
    acquisition_cost = models.PositiveIntegerField(default=0)
    actual_sale = models.PositiveIntegerField(null=True, blank=True)
    tax_percentage = models.FloatField(
        default=1,
        help_text='The percentage of the lot that is taxable (i.e., goods)'
    )
    # tracking
    complete = models.BooleanField(
        default=False,
        help_text='The lot description and items are complete'
    )
    confirmed = models.BooleanField(
        default=False,
        help_text='The items has been reviewed complete and available on-site for sale'
    )
    notes = models.TextField(
        blank=True,
        help_text='Internal notes on the lot'
    )
    auction_contact_point = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def image_thumbnail(self):
        return mark_safe('<img src="/uploads/%s" width="50" height="50" />' % (self.image))
    image_thumbnail.short_description = 'Preview'
    image_thumbnail.allow_tags = True
    def __str__(self):
        return self.auction.abbr + ' - ' + self.type + '-' + str(self.lot_number) + '-' + self.title
    class Meta:
        unique_together = (("auction", "lot_number"),)

class Donation(models.Model):
    auction = models.ForeignKey(
        Auction,
        help_text='The auction currently associated with the donation'
    )
    source_form = models.ForeignKey(
        DonationForm,
        null=True,
        help_text='The donation form'
    )
    form_entry_number = models.PositiveIntegerField(
        help_text='The entry number of the donation form'
    )
    donor_organization = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    donor_name = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    donor_email = models.EmailField(
        null=True,
        blank=True,
    )
    donor_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    donor_address = models.TextField(
        null=True,
        blank=True,
    )
    guardsmen_contact = models.CharField(
        max_length=140,
        null=True,
        blank=True,
    )
    auction_items = models.TextField(
        null=True,
        blank=True,
    )
    auction_description = models.TextField(
        null=True,
        blank=True,
    )
    auction_value = models.FloatField(
        null=True,
        blank=True,
    )
    auction_contact_point = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    delivery_method = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    special_instructions = models.TextField(
        null=True,
        blank=True,
    )
    form_created_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    form_updated_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True,
    )
    inactive_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.auction.abbr + ' - ' + str(self.form_entry_number) + ' - ' + self.donor_organization
    class Meta:
        unique_together = (("source_form", "form_entry_number"),)

LOCATIONS = (
    ('OFFICE', 'Guardsmen Office'),
    ('SFWC', 'SF Wine Center'),
    ('OTHER', 'Other')
)

class Item(models.Model):
    lot = models.ForeignKey(
        Lot,
        null=True,
        blank=True,
    )
    donation = models.ForeignKey(
        Donation,
        null=True,
        blank=True,
        help_text='The donation form submitted for this item'
    )
    description = models.CharField(
        max_length=140,
        help_text='Short description of the item for display and receipt'
    )
    onsite_pickup = models.BooleanField(default=True)
    contact_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='Contact name for bidder questions'
    )
    contact_point = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='Contact point (e.g., phone or email) for contact'
    )
    location = models.CharField(
        max_length=40,
        choices=LOCATIONS,
        default='OTHER',
        help_text='Where the item is currently located'
    )
    location_notes = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    item_notes = models.TextField(
        null=True,
        blank=True,
    )
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
