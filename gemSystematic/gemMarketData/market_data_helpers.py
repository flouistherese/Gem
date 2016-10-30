from gemDatabase.models import *

def get_data_point_types():
	return {x.code:x.id for x in DataPointType.objects.all()}