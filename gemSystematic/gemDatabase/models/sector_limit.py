from django.db import models
from sector import Sector
from limit_type import LimitType
from account import Account

class SectorLimit(models.Model):
  account = models.ForeignKey('Account', blank = False, null = False)
  sector = models.ForeignKey('Sector', blank = False, null = False)
  limit_type = models.ForeignKey('LimitType', blank = False, null = False)
  side = models.CharField(max_length=20, blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="sector_limits"