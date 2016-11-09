from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
import pandas as pd
import cPickle as pickle
import os.path
from gemUtils.utils import default_dated_directory
from gemTradingData.trading_environment import TradingEnvironment

class TradingEnvironmentExport:
	
	@staticmethod
	def export(directory = default_dated_directory()):
		trading_env = TradingEnvironment()

		trading_env.strategies = pd.DataFrame(list(Strategy.objects.values('code', 'description', 'strategy_type__code')))
		trading_env.strategies.rename(columns={'strategy_type__code':'strategy_type'}, inplace=True)

		trading_env.trading_models = pd.DataFrame(list(TradingModel.objects.values('code', 'description', 'strategy__code', 'enabled')))
		trading_env.trading_models.rename(columns={'strategy__code':'strategy'}, inplace=True)

		trading_env.model_feeds = pd.DataFrame(list(TradingModelFeed.objects.values('trading_model__code', 'data_feed__code')))
		trading_env.model_feeds.rename(columns={'trading_model__code':'trading_model', 'data_feed__code':'feed'}, inplace=True)

		trading_env.target_instruments = pd.DataFrame(list(TargetInstrument.objects.values('trading_model__code', 'instrument__code')))
		trading_env.model_feeds.rename(columns={'trading_model__code':'trading_model', 'instrument__code':'instrument'}, inplace=True)

		trading_env.accounts = pd.DataFrame(list(Account.objects.values('code', 'account_group__code', 'account_capital', 'volatility_target')))
		trading_env.accounts.rename(columns={'account_group__code':'account_group'}, inplace=True)

		trading_env.model_limits = pd.DataFrame(list(ModelLimit.objects.values('trading_model__code', 'account__code', 'limit_type__code', 'value')))
		trading_env.model_limits.rename(columns={'trading_model__code':'trading_model', 'account__code':'account', 'limit_type__code':'limit_type'}, inplace=True)

		trading_env.asset_limits = pd.DataFrame(list(AssetLimit.objects.values('instrument_family__code', 'account__code', 'limit_type__code', 'value')))
		trading_env.asset_limits.rename(columns={'instrument_family__code':'instrument_family', 'account__code':'account', 'limit_type__code':'limit_type'}, inplace=True)

		trading_env.sector_limits = pd.DataFrame(list(SectorLimit.objects.values('sector__code', 'account__code', 'limit_type__code', 'value')))
		trading_env.sector_limits.rename(columns={'sector__code':'sector', 'account__code':'account', 'limit_type__code':'limit_type'}, inplace=True)


		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(os.path.join(directory, 'trading_environment'), 'wb') as pickle_file:
			pickle.dump(trading_env, pickle_file, pickle.HIGHEST_PROTOCOL)

		return trading_env