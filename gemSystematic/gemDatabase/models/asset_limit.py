from django.db import models
from instrument_family import InstrumentFamily
from limit_type import LimitType
from account import Account

class AssetLimit(models.Model):
  account = models.ForeignKey('Account', blank = False, null = False)
  instrument_family = models.ForeignKey('InstrumentFamily', blank = False, null = False)
  limit_type = models.ForeignKey('LimitType', blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="asset_limits"