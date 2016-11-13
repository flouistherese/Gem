from django.db import models
from meta_class import ModelMeta
from future import Future
from instrument import Instrument
from currency_pair import CurrencyPair

class DataFeed(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  future = models.ForeignKey('Future', blank = True, null = True)
  currency_pair = models.ForeignKey('CurrencyPair', blank = True, null = True)
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  __metaclass__ = ModelMeta
  class Meta:
        db_table="data_feeds"