from django.db import models
from meta_class import ModelMeta
from trading_model import TradingModel
from data_feed import DataFeed

class TradingModelFeed(models.Model):
  trading_model = models.ForeignKey('TradingModel', blank = False, null = True)
  data_feed = models.ForeignKey('DataFeed', blank = False, null = True)
  
  __metaclass__ = ModelMeta

  class Meta:
        db_table="trading_model_feeds"