from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *
from datetime import timedelta
import pandas as pd
from django_pandas.io import read_frame
from sqlalchemy import create_engine
import pdb

class Command(BaseCommand):
	help = 'Report data points with a zero value'

	def handle(self, *args, **options):
		engine = create_engine('postgresql://gemcorp:azerty@localhost:5432/gem')
		rep = Report(report_date = '2016-10-28', report_type = ReportType["ZERO_VALUE"])
		rep.save()
		zero_value_points = pd.DataFrame(list(DataPoint.objects.filter(value  = 0).values('id')))
		zero_value_points.rename(columns={'id':'data_point_id'}, inplace=True)
		zero_value_points['report_id'] = rep.id
		zero_value_points['ignored'] = False
		zero_value_points.to_sql('report_items',engine, if_exists='append', index = False)