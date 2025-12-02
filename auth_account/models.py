from django.db import models

class BotAuth(models.Model):
    account_id = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    secret_key = models.TextField()
    jwt_token = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.account_id + ' ' + self.description




# class Weekend(models.Model):
#     account_id = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)
