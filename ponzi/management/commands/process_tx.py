from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ponzi.utils import process_tx


class Command(BaseCommand):
    help = 'Processing incoming and outgoing transactions, triggered by walletnotify'

    def handle(self, txid, *args, **options):

        process_tx(txid)

