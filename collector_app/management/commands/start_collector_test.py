from django.core.management.base import BaseCommand, CommandError

from collector_app.services import startCollectorQuoter


class Command(BaseCommand):
    help = 'start_collector_test'

    def handle(self, *args, **options):
        startCollectorQuoter()
