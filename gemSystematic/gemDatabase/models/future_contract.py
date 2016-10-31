from django.db import models
from meta_class import ModelMeta
from instrument import Instrument
from month import Month

class FutureContract(models.Model):
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  future = models.ForeignKey('Future', blank = False, null = True)
  first_trade_date = models.DateField(blank = False, null = False)
  last_trade_date = models.DateField(blank = False, null = False)
  first_notice_date = models.DateField(blank = False, null = False)
  month = models.ForeignKey('Month', blank = False, null = True)
  year = models.IntegerField(blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="future_contracts"

  def next():