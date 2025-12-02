from django.core.management.base import BaseCommand, CommandError

from bund_quoter.services import startBotQuoter


class Command(BaseCommand):
    help = 'start_bot_test'

    def handle(self, *args, **options):
       startBotQuoter()