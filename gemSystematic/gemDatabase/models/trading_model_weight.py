from django.db import models
from account_group import AccountGroup
from trading_model import TradingModel

class TradingModelWeight(models.Model):
  account_group = models.ForeignKey('AccountGroup', blank = False, null = False)
  trading_model = models.ForeignKey('TradingModel', blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="trading_model_weights"