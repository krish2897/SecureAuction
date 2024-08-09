import logging
from celery import shared_task
from django.utils import timezone
from .models import Auction

@shared_task
def check_auctions():
    now = timezone.now()
    logging.info(f"checking auction at {now}")
    auctions_to_close = Auction.objects.filter(ending_date__lte=now, is_closed=False)

    for auction in auctions_to_close:
        logging.info(f"auction: {auction.pk}")
        auction.close_auction()