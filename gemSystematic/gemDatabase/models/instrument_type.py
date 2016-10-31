from django.db import models
from meta_class import ModelMeta

class InstrumentType(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="instrument_types"