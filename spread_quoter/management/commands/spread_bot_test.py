from django.core.management.base import BaseCommand, CommandError

from spread_quoter.services import startSpreadQuoter, startSpreadQuoterSingle


class Command(BaseCommand):
    help = 'spread_bot_test'

    def handle(self, *args, **options):
        unique_id = 'EventSpreadQuoter'
        from spread_quoter.tasks import startSpreadQuoterSingle_Task
        startSpreadQuoterSingle_Task.apply_async(args=[unique_id, 'CRH6CRM6@RTSX'])

        # res = startSpreadQuoterSingle('CRH6CRM6@RTSX')
        # print(res)
