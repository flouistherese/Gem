from __future__ import unicode_literals

from django.db import models

# Create your models here.

class InstrumentType(models.Model):
    code = models.CharField(max_length=200)
    label = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
