from django.db import models
from meta_class import ModelMeta
from instrument_type import InstrumentType

class Instrument(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  instrument_type = models.ForeignKey('InstrumentType', blank = False, null = False)
  #valid_time = models.ValidTime(sequenced_unique=('cat',), current_unique=('cat',))
  __metaclass__ = ModelMeta

  class Meta:
        db_table="instruments" 