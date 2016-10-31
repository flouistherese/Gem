from django.db import models
from meta_class import ModelMeta
from report_type import ReportType

class Report(models.Model):
  report_date = models.DateTimeField(auto_now=True, blank = False, null = False)
  report_type = models.ForeignKey('ReportType', blank = False, null = False)

  class Meta:
        db_table="reports"