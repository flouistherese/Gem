from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
from sqlalchemy import create_engine
from datetime import timedelta
import quandl
import pandas as pd


class MarketDataImport:

	@staticmethod
	def get_futures_contracts_trading():
		return 0


	@staticmethod
	def import_new_contracts():
		futures = list(Future.objects.all())
		futures_contracts = pd.DataFrame(list(FutureContract.objects.values('first_trade_date', 'last_trade_date', 'first_notice_date', 'month__month_code', 'year', 'future__bloomberg_code', 'instrument__code')))

		for fu in futures:
			available_contracts = get_futures_contracts_trading(fu.bloomberg_code)
			comparison = pd.merge(futures_contracts,available_contracts, how='outer', indicator=True)
			missing_contracts = comparison.copy()
			missing_contracts = missing_contracts.loc[missing_contracts['_merge'] != 'both'].drop('_merge', 1)
			if not missing_contracts.empty:
				missing_contracts.rename(columns={'future__bloomberg_code':'future_id', 'month__month_code':'month_id'}, inplace=True)
				missing_contracts['future_id'] = map(lambda x: Future[x].id, missing_contracts['future_id'])
				missing_contracts['month_id'] = map(lambda x: Month.objects.get(month_code = x).id, missing_contracts['month_id'])
				#TODO: Create instruments before creating FutureContracts


	@staticmethod
	def store_market_data(product, response, columns, data_point_types, sql_alchemy_engine):
		if not response.empty:
			response['date'] = response.index
			response = pd.melt(response, id_vars = ['date'], value_vars = columns)
			response['instrument_id'] = product.instrument.id
			response.rename(columns={'variable':'data_point_type_id'}, inplace=True)
			response['data_point_type_id'] = map(lambda x: x.upper().replace (" ", "_"), response['data_point_type_id'])
			response['data_point_type_id'] = response['data_point_type_id'].apply(lambda x: data_point_types[x])
			response['data_point_source_id'] = 1
			response.to_sql('data_points', sql_alchemy_engine, if_exists='append', index = False)
			print "Inserted ",len(response.index)," points for ",product.bloomberg_code

	@staticmethod
	def backfill_stock_data(sql_alchemy_engine, data_point_types = get_data_point_types()):
		print "Downloading and inserting stock data"
		columns = ['Open', 'Low', 'High', 'Close', 'Volume']
		stocks = list(Stock.objects.all())
		for st in stocks:
			existing_data_points = DataPoint.objects.filter(instrument_id = st.instrument.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = st.instrument.id).latest('date').date
				latest_date = str(latest_date + timedelta(days = 1))
			response = quandl.get(st.bloomberg_code, start_date = latest_date)[columns]
			MarketDataImport.store_market_data(st, response, columns, data_point_types, sql_alchemy_engine)

	@staticmethod
	def backfill_future_contract_data(sql_alchemy_engine, data_point_types = get_data_point_types()):
		print "Downloading and inserting futures data"
		columns = ['Open', 'Low', 'High', 'Last', 'Volume', 'Open Interest']
		futures_contracts = list(FutureContract.objects.all())
		for fu in futures_contracts:
			existing_data_points = DataPoint.objects.filter(instrument_id = fu.instrument.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = fu.instrument.id).latest('date').date
				latest_date = str(latest_date + timedelta(days = 1))
			contract = FutureContract.objects.filter(instrument_id = fu.instrument.id).first()
			response = quandl.get(fu.bloomberg_code, start_date = latest_date)[columns]
			response.rename(columns={'Last':'Close'}, inplace=True)
			MarketDataImport.store_market_data(fu, response, ['Open', 'Low', 'High', 'Close', 'Volume', 'Open Interest'], data_point_types, sql_alchemy_engine)

	@staticmethod
	def backfill_feed_data(sql_alchemy_engine, data_point_types = get_data_point_types()):
		print "Downloading and inserting data feed data"
		columns = ['Close']
		data_feeds = list(DataFeed.objects.all())
		for df in data_feeds:
			existing_data_points = DataPoint.objects.filter(instrument_id = df.instrument.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = df.instrument.id).latest('date').date
				latest_date = str(latest_date + timedelta(days = 1))
			response = quandl.get(df.bloomberg_code, start_date = latest_date)[['Last']]
			response.rename(columns={'Last':'Close'}, inplace=True)
			MarketDataImport.store_market_data(df, response, columns, data_point_types, sql_alchemy_engine)


	@staticmethod
	def run_backfill(drop_tables = False):
		engine = create_engine('postgresql://gemcorp:azerty@localhost:5432/gem')
		data_point_types = get_data_point_types()
		if drop_tables:
			print "Erasing data in DataPoint table"
			DataPoint.objects.all().delete()

		MarketDataImport.backfill_stock_data(engine, data_point_types)

		MarketDataImport.backfill_future_contract_data(engine, data_point_types)
		
		MarketDataImport.backfill_feed_data(engine, data_point_types)

		

		