from celery import shared_task

from collector_app.services import startCollectorQuoter, startCursCbr, startCursCbrPlusDay


@shared_task
def startCollectorQuoter_Task():
    rez = startCollectorQuoter()
    return f'start Collecto rQuoter {rez}'


@shared_task
def startCursCbr_Task():
    rez = startCursCbr()
    return f'start Curs Cbr {rez}'


@shared_task
def startCursCbrPlusDay_Task():
    rez = startCursCbrPlusDay()
    return f'start Curs Cbr Plus Day {rez}'



