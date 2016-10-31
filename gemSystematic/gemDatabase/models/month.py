from django.db import models
from meta_class import ModelMeta

class Month(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  month_code = models.CharField(max_length=200, blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="months"