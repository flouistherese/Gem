from django.db import models
from trading_model import TradingModel
from limit_type import LimitType
from account import Account

class ModelLimit(models.Model):
  account = models.ForeignKey('Account', blank = False, null = False)
  trading_model = models.ForeignKey('TradingModel', blank = False, null = False)
  limit_type = models.ForeignKey('LimitType', blank = False, null = False)
  side = models.CharField(max_length=20, blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="model_limits"