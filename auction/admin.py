from django.contrib import admin

from .models import CustomUser, Auction, BidsToAuction

admin.site.register(CustomUser)
admin.site.register(Auction)
admin.site.register(BidsToAuction)