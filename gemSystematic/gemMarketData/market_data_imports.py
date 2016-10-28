from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *
from sqlalchemy import create_engine
from datetime import timedelta
import quandl
import pandas as pd


class MarketDataImport:

	@staticmethod
	def run_backfill(drop_tables = False):
		engine = create_engine('postgresql://gemcorp:azerty@localhost:5432/gem')
		if drop_tables:
			print "Erasing data in DataPoint table"
			DataPoint.objects.all().delete()

		print "Downloading and inserting stock data"
		##Stocks
		stocks = list(Stock.objects.all())
		for st in stocks:
			existing_data_points = DataPoint.objects.filter(instrument_id = st.instrument.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = st.instrument.id).latest('date').date
				latest_date = str(latest_date + timedelta(days = 1))
			response = quandl.get(st.bloomberg_code, start_date = latest_date)[['Open', 'Low', 'High', 'Close', 'Volume']]
			if not response.empty:
				response['date'] = response.index
				response = pd.melt(response, id_vars = ['date'], value_vars = ['Open', 'Low', 'High', 'Close', 'Volume'])
				response['instrument_id'] = st.instrument.id
				response.rename(columns={'variable':'data_point_type_id'}, inplace=True)
				response['data_point_type_id'] = map(lambda x: x.upper(), response['data_point_type_id'])
				response['data_point_type_id'] = response['data_point_type_id'].apply(lambda x: DataPointType[x].id)
				response['data_point_source_id'] = 1
				response.to_sql('data_points',engine, if_exists='append', index = False)
				print "Inserted ",len(response.index)," points for ",st.bloomberg_code

		print "Downloading and inserting futures data"
		#Futures
		futures_contracts_instruments = list(Instrument.objects.filter(instrument_type_id = InstrumentType["FUTURE"].id))
		for fu in futures_contracts_instruments:
			existing_data_points = DataPoint.objects.filter(instrument_id = fu.id)
			latest_date = None
			if existing_data_points:
				latest_date = DataPoint.objects.filter(instrument_id = fu.id).latest('date').date
				latest_date = str(latest_date + timedelta(days = 1))
			contract = FutureContract.objects.filter(instrument_id = fu.id).first()
			future_contract_code = "CME/"+contract.future.bloomberg_code +contract.month.month_code + str(contract.year)
			response = quandl.get(future_contract_code, start_date = latest_date)[['Open', 'Low', 'High', 'Last', 'Volume', 'Open Interest']]
			response.rename(columns={'Last':'Close'}, inplace=True)

			if not response.empty:
				response['date'] = response.index
				response = pd.melt(response, id_vars = ['date'], value_vars = ['Open', 'Low', 'High', 'Close', 'Volume', 'Open Interest'])
				response['instrument_id'] = fu.id
				response.rename(columns={'variable':'data_point_type_id'}, inplace=True)
				response['data_point_type_id'] = map(lambda x: x.upper().replace (" ", "_"), response['data_point_type_id'])
				response['data_point_type_id'] = response['data_point_type_id'].apply(lambda x: DataPointType[x].id)
				response['data_point_source_id'] = 1
				response.to_sql('data_points',engine, if_exists='append', index = False)
				print "Inserted ",len(response.index)," points for ",fu.code
