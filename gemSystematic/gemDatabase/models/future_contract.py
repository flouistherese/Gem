from django.db import models
from meta_class import ModelMeta
from instrument import Instrument
from month import Month
from future_month import FutureMonth

class FutureContract(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  instrument = models.ForeignKey('Instrument', blank = False, null = False)
  future = models.ForeignKey('Future', blank = False, null = True)
  first_trade_date = models.DateField(blank = False, null = False)
  last_trade_date = models.DateField(blank = False, null = False)
  first_notice_date = models.DateField(blank = False, null = False)
  month = models.ForeignKey('Month', blank = False, null = True)
  year = models.IntegerField(blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  __metaclass__ = ModelMeta


  class Meta:
        db_table="future_contracts"

  def next(self):
    generic_months = [o.month for o in list(FutureMonth.objects.filter(future_id = self.future.id))]
    current_month_index = generic_months.index(self.month)
    next_year = self.year
    next_mont = None
    if(current_month_index == len(generic_months) - 1): #If last available month, go to next year
      next_year += 1
      next_month = generic_months[0]
    else:
      next_month = generic_months[current_month_index + 1]

    next_contract = FutureContract(future = self.future, month = next_month, year = next_year)

    return next_contract

  def build_code(self):
    return self.future.code + self.month.month_code + str(self.year)[-2:]