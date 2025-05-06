from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, blank=False, null=False)
    age = models.IntegerField()

class Order(models.Model):
    order = models.CharField(max_length=255, blank=False, null=False)

