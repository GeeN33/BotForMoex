import json

from celery import shared_task
from celery.result import AsyncResult
from django_celery_results.models import TaskResult
import redis

from core.settings import redis_host
from spread_quoter.services import startSpreadQuoterSingle

redis_client = redis.Redis(host=redis_host, port=6379, db=3)



@shared_task
def startSpreadQuoterSingle2_Task(unique_id, symbol):

    name = f'startSpreadQuoterSingle2'
    got_lock = redis_client.set(name=f'{name}-{unique_id}', value=unique_id, ex=10, nx=True)
    if not got_lock:
        return f'{name} Skipp'

    res = startSpreadQuoterSingle(symbol)

    return f'{name}-{symbol}:\n{res}'



@shared_task
def startSpreadQuoterSingle_Task(unique_id, symbol):

    name = f'startSpreadQuoterSingle'
    got_lock = redis_client.set(name=f'{name}-{unique_id}', value=unique_id, ex=10, nx=True)
    if not got_lock:
        startSpreadQuoterSingle2_Task.apply_async(args=[unique_id, symbol], countdown=15)
        return f'{name} Skipp'

    res = startSpreadQuoterSingle(symbol)

    return f'{name}-{symbol}:\n{res}'