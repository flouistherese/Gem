from django.db import models
from instrument_type import InstrumentType

class Rounding(models.Model):
  instrument_type = models.ForeignKey('InstrumentType', blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="roundings"