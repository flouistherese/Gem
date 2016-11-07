from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
import pandas as pd
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory
from gemTradingData.trading_environment import TradingEnvironment

class TradingEnvironmentExport:
	strategies = pd.DataFrame()
	trading_models = pd.DataFrame()
	model_feeds = pd.DataFrame()
	
	@staticmethod
	def export(directory = default_dated_directory()):
		trading_env = TradingEnvironment()

		trading_env.strategies = pd.DataFrame(list(Strategy.objects.values('code', 'description', 'strategy_type__code')))
		trading_env.strategies.rename(columns={'strategy_type__code':'strategy_type'}, inplace=True)

		trading_env.trading_models = pd.DataFrame(list(TradingModel.objects.values('code', 'description', 'strategy__code')))
		trading_env.trading_models.rename(columns={'strategy__code':'strategy'}, inplace=True)

		trading_env.model_feeds = pd.DataFrame(list(TradingModelFeed.objects.values('trading_model__code', 'data_feed__code')))
		trading_env.model_feeds.rename(columns={'trading_model__code':'trading_model', 'data_feed__code':'feed'}, inplace=True)


		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(os.path.join(directory, 'trading_environment'), 'wb') as pickle_file:
			pickle.dump(trading_env, pickle_file, pickle.HIGHEST_PROTOCOL)

		return trading_env