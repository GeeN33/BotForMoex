from django.core.management.base import BaseCommand, CommandError

from option_quoter.optionService import OptionService


class Command(BaseCommand):
    help = 'start_option_test'

    def handle(self, *args, **options):
        option = OptionService()

        # res = option.get_assets()

        res = option.get_option('CNYRUB_TOM', "CR11.6CM6B")

        print(res.theorprice)
