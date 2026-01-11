from django.db import models

from auth_account.models import BotAuth


class ValuteCursCbr(models.Model):
    name = models.CharField(max_length=100)
    nominal = models.IntegerField(default=0, blank=True)
    value = models.FloatField(default=0, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BarCbr(models.Model):
    cbr = models.ForeignKey(ValuteCursCbr, on_delete=models.SET_NULL, null=True)

    last = models.FloatField(default=0, blank=True)

    day1 = models.IntegerField(default=0, blank=True)
    hour1 = models.IntegerField(default=0, blank=True)
    last1 = models.FloatField(default=0, blank=True)

    day2 = models.IntegerField(default=0, blank=True)
    hour2 = models.IntegerField(default=0, blank=True)
    last2 = models.FloatField(default=0, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_at} {self.cbr.name} {self.last} | {self.last1} | {self.last2}'

    class Meta:
        ordering = ['created_at',]


class CollectorQuoter(models.Model):
    auth_bot = models.ForeignKey(BotAuth, on_delete=models.SET_NULL, null=True)
    cbr = models.ForeignKey(ValuteCursCbr, on_delete=models.SET_NULL, null=True)
    symbol_bonds = models.CharField(max_length=100)
    symbol_futures = models.CharField(max_length=100)
    nominal_bonds = models.IntegerField(default=0, blank=True)
    nominal_futures = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=True)


class Bar(models.Model):
    collector = models.ForeignKey(CollectorQuoter, on_delete=models.CASCADE)

    cbr_price = models.FloatField(default=0, blank=True)

    last = models.FloatField(default=0, blank=True)
    ask = models.FloatField(default=0, blank=True)
    bid = models.FloatField(default=0, blank=True)

    last1 = models.FloatField(default=0, blank=True)
    ask1 = models.FloatField(default=0, blank=True)
    bid1 = models.FloatField(default=0, blank=True)

    last2 = models.FloatField(default=0, blank=True)
    ask2 = models.FloatField(default=0, blank=True)
    bid2 = models.FloatField(default=0, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at',]



class BarCbrDay(models.Model):
    cbr = models.ForeignKey(ValuteCursCbr, on_delete=models.CASCADE)
    timestamp = models.IntegerField()

    date_str = models.CharField(max_length=10, default='', blank=True)

    year = models.IntegerField(default=0, blank=True)
    month = models.IntegerField(default=0, blank=True)
    day = models.IntegerField(default=0, blank=True)

    price = models.FloatField(default=0, blank=True)

    class Meta:
        ordering = ['timestamp',]






