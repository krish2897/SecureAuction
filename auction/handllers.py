import logging
import asyncio
from django.dispatch import receiver
from .signals import auction_closed
from .models import Auction, BidsToAuction

from .nillion.libs import compute_result

logger = logging.getLogger(__name__)

@receiver(auction_closed)
def calculate_winner(sender, auction_id, **kwargs):
    auction = Auction.objects.get(id=auction_id)

    store_ids = BidsToAuction.objects.filter(auction=auction).values_list('store_id', flat=True)

    store_id_list = list(store_ids)
    logger.info(f"sore_ids: {store_id_list}")

    output = asyncio.run(compute_result.compute_result(auction.program_id, store_id_list, auction.base_price))

    result = []

    for key, value in output.items():
        if value == 2:
            result.append(int(key.replace('output', '')))

    winner = BidsToAuction.objects.filter(auction=auction).filter(bid_number__in=result).order_by("bidding_date")[0].bidder

    auction.winner = winner
    auction.save()
    

    logger.info(f"output:{output}")