from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
import pandas as pd
from django_pandas.io import read_frame
from datetime import date
import cPickle as pickle

class MarketEnvironment:
	currencies = pd.DataFrame()
	currency_pairs = pd.DataFrame()
	instruments = pd.DataFrame()
	instrument_types = pd.DataFrame()
	exchanges = pd.DataFrame()
	futures = pd.DataFrame()
	future_contracts = pd.DataFrame()
	stock_data = pd.DataFrame()
	feed_data = pd.DataFrame()

	@staticmethod
	def export(directory = default_dated_directory()):
		market_env = MarketEnvironment()

		market_env.currencies = read_frame(Currency.objects.all()).drop('id', 1)

		market_env.instrument_types = read_frame(InstrumentType.objects.all()).drop('id', 1)

		market_env.exchanges = read_frame(Exchange.objects.all()).drop('id', 1)

		market_env.instruments = read_frame(Instrument.objects.all()).drop('id', 1)

		market_env.currency_pairs = pd.DataFrame(list(CurrencyPair.objects.values('code', 'description', 'base_currency__code','quoted_currency__code')))
		market_env.currency_pairs.rename(columns={'base_currency__code':'base_currency', 'quoted_currency__code':'quoted_currency'}, inplace=True)

		market_env.futures = pd.DataFrame(list(Future.objects.values('code', 'description', 'bloomberg_code','minimum_tick_size', 'contract_size','point_value', 'settlement_type__code', 'exchange__code', 'currency__code')))
		market_env.futures.rename(columns={'exchange__code':'exchange', 'currency__code':'currency', 'settlement_type__code':'settlement_type'}, inplace=True)

		market_env.future_contracts = pd.DataFrame(list(FutureContract.objects.values('instrument__code', 'first_trade_date', 'last_trade_date','first_notice_date', 'month__code','year', 'future__code', 'instrument__code')))
		market_env.future_contracts.rename(columns={'instrument__code':'instrument', 'month__code':'month', 'future__code':'future', 'instrument__code':'instrument'}, inplace=True)

		market_env.stock_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'STOCK').values('date', 'value','instrument__code')))
		market_env.stock_data.rename(columns={'instrument__code':'instrument'}, inplace=True)

		market_env.feed_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'DATA_FEED').values('date', 'value','instrument__code')))
		market_env.feed_data.rename(columns={'instrument__code':'feed'}, inplace=True)

		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(os.path.join(directory, 'market_environment'), 'wb') as pickle_file:
			pickle.dump(market_env, pickle_file, pickle.HIGHEST_PROTOCOL)

		return market_env


	@staticmethod
	def load(date_directory = date.today(), file_path = None):
		if file_path is None:
			file_path = os.path.join(default_dated_directory(date_directory), 'market_environment')

		if not os.path.exists(file_path):
			raise Exception('No market environment was found for ' + date_directory)

		with open(file_path, 'rb') as f:
			return pickle.load(f)