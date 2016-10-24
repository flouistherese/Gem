from __future__ import unicode_literals

from django.db import models
from gemDatabase.models import Currency, InstrumentType, Exchange, Instrument, MarketDataPoint
import pandas as pd
from django_pandas.io import read_frame

# Create your models here.

class MarketEnvironment:
	currencies = pd.DataFrame()
	instruments = pd.DataFrame()
	instrument_types = pd.DataFrame()
	exchanges = pd.DataFrame()
	stock_prices = pd.DataFrame()

	@staticmethod
	def export():
		market_env = MarketEnvironment()
		market_env.currencies = read_frame(Currency.objects.all()).drop('id', 1)
		market_env.instrument_types = read_frame(InstrumentType.objects.all()).drop('id', 1)
		market_env.exchanges = read_frame(Exchange.objects.all()).drop('id', 1)
		market_env.instruments = read_frame(Instrument.objects.all()).drop('id', 1)
		market_env.stock_prices = pd.DataFrame(list(MarketDataPoint.objects.filter(data_point_type__code = 'CLOSE').values('date', 'value','instrument__code')))
		
		data_points = read_frame(MarketDataPoint.objects.all()).drop('id', 1)
		return market_env


