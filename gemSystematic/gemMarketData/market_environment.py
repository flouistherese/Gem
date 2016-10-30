from gemDatabase.models import Currency, InstrumentType, Exchange, Instrument, DataPoint, FutureContract
import pandas as pd
from django_pandas.io import read_frame

class MarketEnvironment:
	currencies = pd.DataFrame()
	instruments = pd.DataFrame()
	instrument_types = pd.DataFrame()
	exchanges = pd.DataFrame()
	future_contracts = pd.DataFrame()
	stock_data = pd.DataFrame()
	feed_data = pd.DataFrame()

	@staticmethod
	def export():
		market_env = MarketEnvironment()

		market_env.currencies = read_frame(Currency.objects.all()).drop('id', 1)

		market_env.instrument_types = read_frame(InstrumentType.objects.all()).drop('id', 1)

		market_env.exchanges = read_frame(Exchange.objects.all()).drop('id', 1)

		market_env.instruments = read_frame(Instrument.objects.all()).drop('id', 1)

		market_env.future_contracts = pd.DataFrame(list(FutureContract.objects.values('instrument__code', 'first_trade_date', 'last_trade_date','first_notice_date', 'month__code','year', 'future__code', 'instrument__code')))
		market_env.future_contracts.rename(columns={'instrument__code':'instrument', 'month__code':'month', 'future__code':'future', 'instrument__code':'instrument'}, inplace=True)

		market_env.stock_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'STOCK').values('date', 'value','instrument__code')))
		market_env.stock_data.rename(columns={'instrument__code':'instrument'}, inplace=True)

		market_env.feed_data = pd.DataFrame(list(DataPoint.objects.filter(data_point_type__code = 'CLOSE', instrument__instrument_type__code = 'DATA_FEED').values('date', 'value','instrument__code')))
		market_env.feed_data.rename(columns={'instrument__code':'feed'}, inplace=True)

		return market_env