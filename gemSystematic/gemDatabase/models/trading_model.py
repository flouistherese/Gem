from django.db import models
from meta_class import ModelMeta
from strategy import Strategy

class TradingModel(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  strategy = models.ForeignKey('Strategy', blank = False, null = True)
  enabled = models.BooleanField(default = True)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="trading_models"