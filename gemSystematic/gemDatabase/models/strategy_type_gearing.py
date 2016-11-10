from django.db import models
from account_group import AccountGroup
from strategy_type import StrategyType

class StrategyTypeGearing(models.Model):
  account_group = models.ForeignKey('AccountGroup', blank = False, null = False)
  strategy_type = models.ForeignKey('StrategyType', blank = False, null = False)
  value = models.DecimalField(max_digits=30, decimal_places=10, blank = False, null = True)

  class Meta:
        db_table="strategy_type_gearings"