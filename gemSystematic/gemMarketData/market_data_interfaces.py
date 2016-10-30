from django.core.management.base import BaseCommand, CommandError
from gemMarketData.market_data_helpers import *
import pandas as pd
import quandl
from datetime import date


class QuandlInterface:
	quandl.ApiConfig.api_key = 'JyPzgcScbDfyY5H-mVhM' 

	def get_historical_data(ticker, fields, start_date = None, end_date = str(date.today()))
		response = quandl.get(tickers, start_date = start_date, end_date = end_date)[fields]