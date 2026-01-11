import uuid
from django.db import models

from auth_account.models import BotAuth


class BotQuoterOption(models.Model):

    auth_bot = models.ForeignKey(BotAuth, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
