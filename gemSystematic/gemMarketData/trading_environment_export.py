from gemDatabase.models import *
from gemMarketData.market_data_helpers import *
import pandas as pd
import cPickle as pickle
import os.path
from decimal import *
from gemUtils.utils import default_dated_directory
from gemTradingData.trading_environment import TradingEnvironment

class TradingEnvironmentExport:
	
	@staticmethod
	def export(directory = default_dated_directory()):
		trading_env = TradingEnvironment()

		#Accounts
		trading_env.accounts = pd.DataFrame(list(Account.objects.values('code', 'account_group__code', 'account_capital', 'volatility_target')))
		trading_env.accounts.rename(columns={'code':'account','account_group__code':'account_group'}, inplace=True)
		trading_env.accounts['scaling'] = (trading_env.accounts['account_capital'].astype('float64') / 100E6) * (trading_env.accounts['volatility_target'].astype('float64')/ 0.15)

		#Models
		trading_env.strategies = pd.DataFrame(list(Strategy.objects.values('code', 'strategy_type__code')))
		trading_env.strategies.rename(columns={'code':'strategy','strategy_type__code':'strategy_type'}, inplace=True)

		trading_env.trading_models = pd.DataFrame(list(TradingModel.objects.values('code', 'strategy__code', 'enabled')))
		trading_env.trading_models.rename(columns={'code':'trading_model','strategy__code':'strategy'}, inplace=True)

		trading_env.model_feeds = pd.DataFrame(list(TradingModelFeed.objects.values('trading_model__code', 'data_feed__code')))
		trading_env.model_feeds.rename(columns={'trading_model__code':'trading_model', 'data_feed__code':'feed'}, inplace=True)

		#Instruments
		trading_env.target_instruments = pd.DataFrame(list(TargetInstrument.objects.values('trading_model__code', 'instrument__code')))
		trading_env.target_instruments.rename(columns={'trading_model__code':'trading_model', 'instrument__code':'instrument'}, inplace=True)

		#Limits
		trading_env.model_limits = pd.DataFrame(list(ModelLimit.objects.values('trading_model__code', 'account__code', 'limit_type__code', 'side', 'value')))
		trading_env.model_limits.rename(columns={'trading_model__code':'trading_model', 'account__code':'account', 'limit_type__code':'limit_type', 'value':'limit'}, inplace=True)

		trading_env.asset_limits = pd.DataFrame(list(AssetLimit.objects.values('instrument_family__code', 'account__code', 'limit_type__code', 'side', 'value')))
		trading_env.asset_limits.rename(columns={'instrument_family__code':'instrument_family', 'account__code':'account', 'limit_type__code':'limit_type', 'value':'limit'}, inplace=True)

		trading_env.sector_limits = pd.DataFrame(list(SectorLimit.objects.values('sector__code', 'account__code', 'limit_type__code', 'side', 'value')))
		trading_env.sector_limits.rename(columns={'sector__code':'sector', 'account__code':'account', 'limit_type__code':'limit_type', 'value':'limit'}, inplace=True)

		trading_env.roundings = pd.DataFrame(list(Rounding.objects.values('instrument_type__code', 'value')))
		trading_env.roundings.rename(columns={'instrument_type__code':'instrument_type', 'value':'rounding'}, inplace=True)

		#Portfolio Tree
		trading_env.portfolio_gearings = pd.DataFrame(list(PortfolioGearing.objects.values('account_group__code', 'value')))
		trading_env.portfolio_gearings.rename(columns={'account_group__code':'account_group','value':'portfolio_gearing'}, inplace=True)

		trading_env.strategy_types_gearings = pd.DataFrame(list(StrategyTypeGearing.objects.values('account_group__code', 'strategy_type__code', 'value')))
		trading_env.strategy_types_gearings.rename(columns={'account_group__code':'account_group', 'strategy_type__code':'strategy_type','value':'strategy_types_gearing'}, inplace=True)

		trading_env.strategy_gearings = pd.DataFrame(list(StrategyGearing.objects.values('account_group__code', 'strategy__code', 'value')))
		trading_env.strategy_gearings.rename(columns={'account_group__code':'account_group', 'strategy__code':'strategy','value':'strategy_gearing'}, inplace=True)
		trading_env.strategy_gearings = trading_env.strategy_gearings.merge(trading_env.strategies[['strategy','strategy_type']])

		trading_env.strategy_types_weights = pd.DataFrame(list(StrategyTypeWeight.objects.values('account_group__code', 'strategy_type__code', 'value')))
		trading_env.strategy_types_weights.rename(columns={'account_group__code':'account_group', 'strategy_type__code':'strategy_type','value':'strategy_types_weight'}, inplace=True)

		trading_env.strategy_weights = pd.DataFrame(list(StrategyWeight.objects.values('account_group__code', 'strategy__code', 'value')))
		trading_env.strategy_weights.rename(columns={'account_group__code':'account_group', 'strategy__code':'strategy','value':'strategy_weight'}, inplace=True)
		trading_env.strategy_weights = trading_env.strategy_weights.merge(trading_env.strategies[['strategy','strategy_type']])

		trading_env.model_weights = pd.DataFrame(list(TradingModelWeight.objects.values('account_group__code', 'trading_model__code', 'value')))
		trading_env.model_weights.rename(columns={'account_group__code':'account_group', 'trading_model__code':'trading_model','value':'model_weight'}, inplace=True)
		trading_env.model_weights = trading_env.model_weights.merge(trading_env.trading_models[['strategy','trading_model']])

		if not os.path.exists(directory):
			os.makedirs(directory)

		with open(os.path.join(directory, 'trading_environment'), 'wb') as pickle_file:
			pickle.dump(trading_env, pickle_file, pickle.HIGHEST_PROTOCOL)

		return trading_env