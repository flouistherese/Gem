from django.db import models
from meta_class import ModelMeta
from instrument import Instrument
from currency import Currency

class Stock(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  company = models.CharField(max_length=200, blank = False, null = False)
  currency = models.ForeignKey('Currency', blank = False, null = False)
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="stocks"