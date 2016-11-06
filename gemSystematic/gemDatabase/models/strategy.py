from django.db import models
from meta_class import ModelMeta

class Strategy(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  strategy_type = models.ForeignKey('StrategyType', blank = False, null = True)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="strategies"