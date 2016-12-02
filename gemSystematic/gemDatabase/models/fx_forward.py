from django.db import models
from meta_class import ModelMeta
from currency_pair import CurrencyPair
from instrument import Instrument

class FxForward(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  currency_pair = models.ForeignKey('CurrencyPair', blank = False, null = False)
  notional_currency = models.ForeignKey('Currency', blank = False, null = False)
  contract_date = models.DateField(blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="fx_forwards"