from __future__ import unicode_literals

from django.db import models
#from django_temporal.db import models
from django.db.models.base import ModelBase

class ModelMeta(ModelBase):
	def __getitem__(self, key):
		obj = self.objects.get(code = key)
		print obj.__dict__
		return obj

# Create your models here.

class InstrumentType(models.Model):
  code = models.CharField(max_length=200, blank = False, null = False)
  label = models.CharField(max_length=200, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

class InstrumentType(models.Model):
  code = models.CharField(max_length=200, blank = False, null = False)
  label = models.CharField(max_length=200, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

class Instrument(models.Model):
  code = models.CharField(max_length=200, blank = False, null = False)
  label = models.CharField(max_length=200, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  instrument_type = models.ForeignKey(InstrumentType, blank = False, null = False)
  #valid_time = models.ValidTime(sequenced_unique=('cat',), current_unique=('cat',))
  __metaclass__ = ModelMeta

