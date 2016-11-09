# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gemDatabase', '0027_addStrategies2'),
    ]

    operations = [
        migrations.CreateModel(
            name='TargetInstrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.Instrument')),
                ('trading_model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.TradingModel')),
            ],
            options={
                'db_table': 'target_instruments',
            },
        ),
    ]