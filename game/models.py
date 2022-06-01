from django.db import models


class Stone(models.Model):
    name = models.CharField()
    hex = models.CharField(max_length=6)


class Field(models.Model):
    field = models.CharField(max_length=2)
    value = models.CharField(max_length=6)


class Status