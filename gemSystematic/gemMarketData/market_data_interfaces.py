from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import quandl
from datetime import date
import pdb

class QuandlInterface:
	quandl.ApiConfig.api_key = 'JyPzgcScbDfyY5H-mVhM' 

	def get_historical_data(self, ticker, fields, start_date = None, end_date = str(date.today())):
		response = quandl.get(ticker, start_date = start_date, end_date = end_date)
		headers = list(response.columns.values)
		if 'Last' in headers:
			response.rename(columns={'Last':'Close'}, inplace=True)
		elif 'Value' in headers:
			response.rename(columns={'Value':'Close'}, inplace=True)

		return response[fields]

	def retrieve_contract_information(self, contract):
		#TODO
		#Should raise when no information is found
		raise 'Function retrieve_contract_information() is not implemented yet for Quandl interface'