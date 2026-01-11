from django.core.management.base import BaseCommand, CommandError

from collector_app.bar_cbr_day import run_bar_cbr_day


class Command(BaseCommand):
    help = 'bar_cbr_day_test'

    def handle(self, *args, **options):
        run_bar_cbr_day()