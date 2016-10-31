from django.db import models
from meta_class import ModelMeta
from future import Future
from stock import Stock

class InstrumentFamily(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  future = models.ForeignKey('Future', blank = False, null = True)
  stock = models.ForeignKey('Stock', blank = False, null = True)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="instrument_families"