from django.db import models
from meta_class import ModelMeta
from currency import Currency
from instrument import Instrument

class CurrencyPair(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  pip_size = models.DecimalField(max_digits=11, decimal_places=8, blank = False, null = False)
  base_currency = models.ForeignKey('Currency', blank = False, null = False, related_name='base_currency')
  quoted_currency = models.ForeignKey('Currency', blank = False, null = False, related_name='quoted_currency')
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="currency_pairs"