# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-22 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gemDatabase', '0004_auto_20161022_1338'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='currency',
            table='currencies',
        ),
        migrations.AlterModelTable(
            name='currencypair',
            table='currency_pairs',
        ),
        migrations.AlterModelTable(
            name='datapointsource',
            table='data_point_sources',
        ),
        migrations.AlterModelTable(
            name='datapointtype',
            table='data_point_types',
        ),
        migrations.AlterModelTable(
            name='exchange',
            table='exchanges',
        ),
        migrations.AlterModelTable(
            name='future',
            table='futures',
        ),
        migrations.AlterModelTable(
            name='instrument',
            table='instruments',
        ),
        migrations.AlterModelTable(
            name='instrumenttype',
            table='instrument_types',
        ),
        migrations.AlterModelTable(
            name='marketdatapoint',
            table='market_data_points',
        ),
        migrations.AlterModelTable(
            name='settlementtype',
            table='settlement_types',
        ),
    ]
