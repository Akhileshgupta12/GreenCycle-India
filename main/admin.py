
from django.contrib import admin
from .models import Contact
from django.utils.html import format_html

from .models import AdminNotification


from .models import (
    User,
    Waste,
    Buyer,
    BuyRequest,
    WastePrice
)

admin.site.register(User)

# ---------------- WASTE ADMIN ---------------- #

class WasteAdmin(admin.ModelAdmin):

    list_display = (
        'image_tag',
        'name',
        'material',
        'quantity',
        'price',
        'city',
        'state',
        'status'
    )

    list_display_links = ('name',)

    list_editable = ('status',)

    def image_tag(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="80" height="80" style="border-radius:10px;" />',
                obj.image.url
            )

        return "No Image"

    image_tag.short_description = 'Image'

admin.site.register(Waste, WasteAdmin)

# ---------------- BUYER ADMIN ---------------- #

admin.site.register(Buyer)

# ---------------- BUY REQUEST ADMIN ---------------- #

class BuyRequestAdmin(admin.ModelAdmin):

    list_display = (
        'buyer_name',
        'waste',
        'quantity',
        'status',
        'created_at'
    )

    list_editable = ('status',)

admin.site.register(BuyRequest, BuyRequestAdmin)

# ---------------- WASTE PRICE ADMIN ---------------- #

admin.site.register(WastePrice)

admin.site.register(Contact)

admin.site.register(AdminNotification)