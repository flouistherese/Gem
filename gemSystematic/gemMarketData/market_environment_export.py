from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
import pandas as pd
from django_pandas.io import read_frame
from datetime import date
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory
from gemMarketData.market_environment import MarketEnvironment

class MarketEnvironmentExport:

	@staticmethod
	def export(directory = default_dated_directory()):
		market_env = MarketEnvironment()

		market_env.currencies = read_frame(Currency.objects.all()).drop('id', 1)

		market_env.exchanges = read_frame(Exchange.objects.all()).drop('id', 1)

		market_env.instruments = extract_instruments()

		market_env.instrument_families = pd.DataFrame(list(InstrumentFamily.objects.values('code', 'sector__code')))
		market_env.instrument_families.rename(columns={'code':'instrument_family', 'sector__code':'sector'}, inplace=True)

		market_env.currency_pairs = pd.DataFrame(list(CurrencyPair.objects.values('code', 'base_currency__code','quoted_currency__code')))
		market_env.currency_pairs.rename(columns={'code':'currency_pair', 'base_currency__code':'base_currency', 'quoted_currency__code':'quoted_currency'}, inplace=True)

		market_env.futures = pd.DataFrame(list(Future.objects.values('code', 'bloomberg_code','minimum_tick_size', 'contract_size','point_value', 'settlement_type__code', 'exchange__code', 'currency__code')))
		market_env.futures.rename(columns={'code':'future', 'exchange__code':'exchange', 'currency__code':'currency', 'settlement_type__code':'settlement_type'}, inplace=True)

		market_env.future_contracts = pd.DataFrame(list(FutureContract.objects.values('instrument__code', 'first_trade_date', 'last_trade_date','first_notice_date', 'month__code','year', 'future__code', 'instrument__code')))
		market_env.future_contracts.rename(columns={'instrument__code':'instrument', 'month__code':'month', 'future__code':'future', 'instrument__code':'instrument'}, inplace=True)

		market_env.stocks = pd.DataFrame(list(Stock.objects.values('code', 'bloomberg_code','company', 'currency__code', 'instrument__code')))
		market_env.stocks.rename(columns={'code':'stock', 'currency__code':'currency', 'instrument__code':'instrument'}, inplace=True)

		market_env.stock_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'STOCK').values('date', 'value','instrument__code')))
		market_env.stock_data.rename(columns={'instrument__code':'instrument'}, inplace=True)

		#TODO: Gotta have adjusted and non-adjusted feed
		market_env.feed_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'DATA_FEED').values('date', 'value','instrument__code')))
		market_env.feed_data.rename(columns={'instrument__code':'feed'}, inplace=True)

		market_env.fx_forwards = pd.DataFrame(list(FxForward.objects.values('instrument__code', 'currency_pair__code', 'notional_currency__code','contract_date')))
		market_env.fx_forwards.rename(columns={'instrument__code':'instrument','currency_pair__code':'currency_pair', 'notional_currency__code':'notional_currency'}, inplace=True)

		market_env.fx_spot = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'FX_SPOT').values('date', 'value','instrument__code')))
		market_env.fx_spot.rename(columns={'instrument__code':'feed'}, inplace=True)

		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(os.path.join(directory, 'market_environment'), 'wb') as pickle_file:
			pickle.dump(market_env, pickle_file, pickle.HIGHEST_PROTOCOL)

		return market_env

def extract_instruments():
		##Future Contracts
		instruments = pd.DataFrame()
		future_contracts = list(FutureContract.objects.all())
		for fc in future_contracts:
			new_instrument = pd.DataFrame({'instrument':[fc.instrument.code], 'instrument_type':[fc.instrument.instrument_type.code], 'instrument_family':[InstrumentFamily.objects.get(future_id = fc.future.id).code]})
			instruments = pd.concat([instruments, new_instrument])

		#FX Forwards
		fx_forwards = list(FxForward.objects.all())
		for ff in fx_forwards:
			new_instrument = pd.DataFrame({'instrument':[ff.instrument.code], 'instrument_type':[ff.instrument.instrument_type.code], 'instrument_family':[InstrumentFamily.objects.get(currency_pair_id = ff.currency_pair.id).code]})
			instruments = pd.concat([instruments, new_instrument])

		#Stocks
		stocks = list(Stock.objects.all())
		for s in stocks:
			new_instrument = pd.DataFrame({'instrument':[s.instrument.code], 'instrument_type':[s.instrument.instrument_type.code], 'instrument_family':[InstrumentFamily.objects.get(stock_id = s.id).code]})
			instruments = pd.concat([instruments, new_instrument])

		#Data Feeds
		data_feeds = list(DataFeed.objects.all())
		for df in data_feeds:
			instrument_family = None 
			if not (df.future is None):
				instrument_family = InstrumentFamily.objects.get(future_id = df.future.id).code
			elif not (df.currency_pair is None):
				instrument_family = InstrumentFamily.objects.get(currency_pair_id = df.currency_pair.id).code

			new_instrument = pd.DataFrame({'instrument':[df.instrument.code], 'instrument_type':[df.instrument.instrument_type.code], 'instrument_family':[instrument_family]})
			instruments = pd.concat([instruments, new_instrument])
		
		return instruments.reset_index(drop = True)
