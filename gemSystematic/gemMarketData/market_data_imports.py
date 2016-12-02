from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
from gemMarketData.market_data_interfaces import *
from sqlalchemy import create_engine
from datetime import timedelta
import pandas as pd
import pdb


class MarketDataImport:

	@staticmethod
	def get_futures_contracts_trading():
		return 0


	@staticmethod
	def import_new_contracts():
		futures = list(Future.objects.all())
		futures_contracts = pd.DataFrame(list(FutureContract.objects.values('first_trade_date', 'last_trade_date', 'first_notice_date', 'month__month_code', 'year', 'future__bloomberg_code', 'instrument__code')))

		for fu in futures:
			fu.populate_new_contracts()


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
	def backfill_data(products, columns, sql_alchemy_engine, data_point_types = get_data_point_types(), market_data_interface = QuandlInterface()):
		#pdb.set_trace()
		for p in products:
			existing_data_points = DataPoint.objects.filter(instrument_id = p.instrument.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = p.instrument.id).latest('date').date
				if(latest_date == date.today()):
					return
				latest_date = str(latest_date + timedelta(days = 1))

			response = market_data_interface.get_historical_data(p.bloomberg_code, columns, latest_date)
			MarketDataImport.store_market_data(p, response, columns, data_point_types, sql_alchemy_engine)


	@staticmethod
	def run_backfill(drop_tables = False, market_data_interface = QuandlInterface()):
		engine = create_engine('postgresql://gemcorp:azerty@localhost:5432/gem')
		data_point_types = get_data_point_types()
		if drop_tables:
			print "Erasing data in DataPoint table"
			DataPoint.objects.all().delete()

		stock_columns = ['Open', 'Low', 'High', 'Close', 'Volume']
		future_contracts_columns = ['Open', 'Low', 'High', 'Close', 'Volume', 'Open Interest']
		data_feed_columns = ['Close']
		currency_pair_columns = ['Close']

		MarketDataImport.backfill_data(list(Stock.objects.all()), stock_columns, engine, data_point_types, market_data_interface)

		MarketDataImport.backfill_data(list(FutureContract.objects.all()), future_contracts_columns,  engine, data_point_types, market_data_interface)
		
		MarketDataImport.backfill_data(list(DataFeed.objects.all()), data_feed_columns, engine, data_point_types, market_data_interface)

		MarketDataImport.backfill_data(list(CurrencyPair.objects.all()), currency_pair_columns, engine, data_point_types, market_data_interface)

		

		