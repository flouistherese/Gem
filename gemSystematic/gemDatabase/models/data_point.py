from django.db import models
from meta_class import ModelMeta
from instrument import Instrument
from data_point_source import DataPointSource
from data_point_type import DataPointType

class DataPoint(models.Model):
  instrument = models.ForeignKey('Instrument', blank = False, null = True)
  date = models.DateField(blank = False, null = False)
  data_point_source = models.ForeignKey('DataPointSource', blank = False, null = False)
  data_point_type = models.ForeignKey('DataPointType', blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="data_points"