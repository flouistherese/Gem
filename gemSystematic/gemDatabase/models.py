from __future__ import unicode_literals

from django.db import models
#from django_temporal.db import models
from django.db.models.base import ModelBase

class ModelMeta(ModelBase):
	def __getitem__(self, key):
		obj = self.objects.get(code = key)
		return obj

# Create your models here.

class InstrumentType(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="instrument_types"

class DataPointType(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="data_point_types"

class DataPointSource(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="data_point_sources"

class Exchange(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="exchanges"

class Currency(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="currencies"

class SettlementType(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="settlement_types"

class CurrencyPair(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  pip_size = models.DecimalField(max_digits=11, decimal_places=8, blank = False, null = False)
  base_currency = models.ForeignKey(Currency, blank = False, null = False, related_name='base_currency')
  quoted_currency = models.ForeignKey(Currency, blank = False, null = False, related_name='quoted_currency')
  __metaclass__ = ModelMeta

  class Meta:
        db_table="currency_pairs"

class Instrument(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  instrument_type = models.ForeignKey(InstrumentType, blank = False, null = False)
  #valid_time = models.ValidTime(sequenced_unique=('cat',), current_unique=('cat',))
  __metaclass__ = ModelMeta

  class Meta:
        db_table="instruments"


class Future(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  minimum_tick_size = models.DecimalField(max_digits=9, decimal_places=5, blank = False, null = False)
  contract_size = models.IntegerField(blank = False, null = False)
  point_value = models.DecimalField(max_digits=9, decimal_places=2, blank = False, null = False)
  settlement_type = models.ForeignKey(SettlementType, blank = False, null = False)
  exchange = models.ForeignKey(Exchange, blank = False, null = False)
  currency = models.ForeignKey(Currency, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="futures"

class MarketDataPoint(models.Model):
  instrument = models.ForeignKey(Instrument, blank = False, null = False)
  data_point_source = models.ForeignKey(DataPointSource, blank = False, null = False)
  data_point_type = models.ForeignKey(DataPointType, blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="market_data_points"
