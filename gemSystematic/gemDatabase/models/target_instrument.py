from django.db import models
from trading_model import TradingModel
from instrument import Instrument

class TargetInstrument(models.Model):
  trading_model = models.ForeignKey('TradingModel', blank = False, null = True)
  instrument = models.ForeignKey('Instrument', blank = False, null = True)

  class Meta:
        db_table="target_instruments"