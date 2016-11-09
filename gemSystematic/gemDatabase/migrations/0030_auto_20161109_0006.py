# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 00:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gemDatabase', '0029_addTargetInstruments'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=10, max_digits=30, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.Account')),
                ('instrument_family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.InstrumentFamily')),
            ],
            options={
                'db_table': 'asset_limits',
            },
        ),
        migrations.CreateModel(
            name='LimitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'limit_types',
            },
        ),
        migrations.CreateModel(
            name='ModelLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=10, max_digits=30, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.Account')),
                ('limit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.LimitType')),
                ('trading_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.TradingModel')),
            ],
            options={
                'db_table': 'model_limits',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'sectors',
            },
        ),
        migrations.AddField(
            model_name='assetlimit',
            name='limit_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.LimitType'),
        ),
        migrations.AddField(
            model_name='instrumentfamily',
            name='sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gemDatabase.Sector'),
        ),
    ]
