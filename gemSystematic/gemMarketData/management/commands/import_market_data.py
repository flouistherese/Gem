from django.core.management.base import BaseCommand, CommandError
from gemDatabase.models import *

class Command(BaseCommand):
	help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

	def handle(self, *args, **options):
		print "IMPOOOOORTT THAT SHIT", InstrumentType["ETF"].description, "YEEAAHH" 