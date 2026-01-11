import uuid
from datetime import datetime

from django.db import models

from auth_account.models import BotAuth


class BotQuoterSpread(models.Model):
    CHOICES_SIDE = (
        ('b', 'b'),
        ('s', 's'),
        ('n', 'n'),)

    auth_bot = models.ForeignKey(BotAuth, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    symbolA = models.CharField(max_length=100)
    symbolB = models.CharField(max_length=100)
    symbolC = models.CharField(max_length=100)

    symbolCB = models.CharField(max_length=100)

    sideCB = models.CharField(help_text="side", max_length=30, choices=CHOICES_SIDE)
    quantityB = models.FloatField(default=0)
    quantityC = models.FloatField(default=0)
    quantityCB = models.FloatField(default=0)

    step_price = models.FloatField(default=0)
    step_quantity = models.FloatField(default=0)
    max_quantity = models.FloatField(default=0)



    ask = models.FloatField(default=0, null=True, blank=True)
    last = models.FloatField(default=0, null=True, blank=True)
    bid = models.FloatField(default=0, null=True, blank=True)

    ema = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name

class OrderSmartSpread(models.Model):
    CHOICES_SIDE = (
        ('b', 'b'),
        ('s', 's'),)

    bot = models.ForeignKey(BotQuoterSpread, on_delete=models.CASCADE, null=True, blank=True)

    level_id = models.IntegerField(default=0, blank=True)
    level_queue = models.IntegerField(default=0, blank=True)

    level_price = models.FloatField(default=0, null=True, blank=True)
    level_step = models.FloatField(default=0)
    level_side = models.CharField(help_text="side", max_length=30, choices=CHOICES_SIDE)
    level_quantity = models.FloatField(default=0, null=True, blank=True)

    order_id = models.CharField(max_length=100, default='', null=True, blank=True)
    client_order_id = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.CharField(max_length=100, default='', null=True, blank=True)
    order_type = models.CharField(max_length=100, default='', null=True, blank=True)
    side = models.CharField(max_length=100, default='', null=True, blank=True)
    limit_price = models.FloatField(default=0, null=True, blank=True)
    quantity = models.FloatField(default=0, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ('level_id',)

    def save(self, *args, **kwargs):
        if not self.client_order_id:
            self.client_order_id = str(datetime.utcnow().timestamp())

        super().save(*args, **kwargs)

    def __str__(self):

        res = str(self.level_id) + ' '
        res += str(self.level_queue) + ' '
        res += self.bot.name + ' '
        res += str(self.level_price) + ' '
        res += str(self.level_quantity) + ' '
        res += str(self.level_step) + ' '
        res += str(self.level_side) + ' '
        res += str(self.is_active)

        return res
