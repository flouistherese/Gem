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
    count = 0
    contracts = FutureContract.objects.filter(future_id = self.id)

    if(len(contracts) != 0):
      new_contract = contracts.latest('last_trade_date')
      while True:
        try:
          new_contract = market_data_interface.retrieve_contract_information(new_contract.next())
          new_instrument = Instrument(code = new_contract.code, instrument_type = InstrumentType["FUTURE_CONTRACT"], description = new_contract.future.description + " contract " + new_contract.month.description + " " + str(new_contract.year))
          new_instrument.save()
          new_contract.instrument = Instrument[new_instrument.code]
          new_contract.save()
          count +=1
          print "Imported new contract " + new_contract.code
        except:
          break
    else:
      #TODO: Import all contracts from future
      print "Cant import new contracts: no contract exists for future " + self.code
    print "Imported " + str(count) + " contracts for future " + self.code


  def import_generic_months():
    #TODO
    return 0