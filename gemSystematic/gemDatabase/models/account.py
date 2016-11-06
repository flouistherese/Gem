from django.db import models
from meta_class import ModelMeta
from account_group import AccountGroup


class Account(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  account_capital = models.DecimalField(max_digits=15, decimal_places=4, blank = False, null = False)
  volatility_target = models.DecimalField(max_digits=4, decimal_places=3, blank = False, null = False)
  account_group = models.ForeignKey('AccountGroup', blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="accounts"
