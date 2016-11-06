from gemDatabase.models import *
from datetime import date
import os.path

def get_data_point_types():
	return {x.code:x.id for x in DataPointType.objects.all()}

def default_dated_directory(date = date.today()):
	return str(os.path.join('/home/florian/Dropbox/Code/Gem/market_environment', str(date)))

