from django.db import models
from meta_class import ModelMeta
from report import Report
from data_point import DataPoint

class ReportItem(models.Model):
  data_point = models.ForeignKey('DataPoint', blank = False, null = False)
  report = models.ForeignKey('Report', blank = False, null = False)
  ignored = models.BooleanField(default = False)
  z_score = models.DecimalField(max_digits=8, decimal_places=4, blank = False, null = True)
  class Meta:
        db_table="report_items"