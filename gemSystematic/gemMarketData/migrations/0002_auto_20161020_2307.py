# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-20 23:07
from __future__ import unicode_literals

from django.db import models, migrations
from gemMarketData.models import *
def populate_instrument_type(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    InstrumentType(code = "FUTURE", label="Future", description = "Future")
    InstrumentType(code = "FX_FORWARD", label="FX Forward", description = "FX Forward")


class Migration(migrations.Migration):

    dependencies = [
        ('gemMarketData', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(populate_instrument_type),
    ]
