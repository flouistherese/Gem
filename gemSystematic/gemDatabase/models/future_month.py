from django.db import models
from meta_class import ModelMeta
from month import Month

class FutureMonth(models.Model):
  future = models.ForeignKey('Future', blank = False, null = True)
  month = models.ForeignKey('Month', blank = False, null = True)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="future_months"