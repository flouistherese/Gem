from django.db import models
from meta_class import ModelMeta
from settlement_type import SettlementType
from exchange import Exchange
from currency import Currency
from gemMarketData.market_data_interfaces import *
from future_contract import FutureContract

class Future(models.Model):
  code = models.CharField(max_length=20, blank = False, null = False)
  description = models.CharField(max_length=200, blank = False, null = False)
  bloomberg_code = models.CharField(max_length=20, blank = False, null = False)
  minimum_tick_size = models.DecimalField(max_digits=9, decimal_places=5, blank = False, null = False)
  contract_size = models.IntegerField(blank = False, null = False)
  point_value = models.DecimalField(max_digits=9, decimal_places=2, blank = False, null = False)
  settlement_type = models.ForeignKey('SettlementType', blank = False, null = False)
  exchange = models.ForeignKey('Exchange', blank = False, null = False)
  currency = models.ForeignKey('Currency', blank = False, null = False)
  __metaclass__ = ModelMeta

  class Meta:
        db_table="futures"

  def populate_new_contracts(self, market_data_interface = QuandlInterface()):
    latest_contract = FutureContract.objects.filter(future_id = self.id).latest('last_trade_date')