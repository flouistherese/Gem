from gemDatabase.models import *
from datetime import date

def get_data_point_types():
	return {x.code:x.id for x in DataPointType.objects.all()}

