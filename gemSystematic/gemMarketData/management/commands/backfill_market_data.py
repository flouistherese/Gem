from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *
from sqlalchemy import create_engine
import quandl
import pandas as pd
import pdb;

class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

	def handle(self, *args, **options):
		# stocks = list(Stock.objects.all().values_list('bloomberg_code', flat =True))
		engine = create_engine('postgresql://gemcorp:azerty@localhost:5432/gem')

		MarketDataPoint.objects.all().delete()
		stocks = list(Stock.objects.all())
		for s in stocks:
			response = quandl.get(s.bloomberg_code)[['Open', 'Low', 'High', 'Close', 'Volume']]
			response['date'] = response.index
			response = pd.melt(response, id_vars = ['date'], value_vars = ['Open', 'Low', 'High', 'Close', 'Volume'])
			response['instrument_id'] = s.instrument.id
			response.rename(columns={'variable':'data_point_type_id'}, inplace=True)
			response['data_point_type_id'] = map(lambda x: x.upper(), response['data_point_type_id'])
			response['data_point_type_id'] = response['data_point_type_id'].apply(lambda x: DataPointType[x].id)
			response['data_point_source_id'] = 1
			response.to_sql('market_data_points',engine, if_exists='append', index = False)
			print response.head()
