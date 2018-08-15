# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 11:39
# flake8: noqa
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations, models
from corehq.sql_db.operations import RawSQLMigration


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0055_merge_20180719_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateCcsRecordTHRForms',
            fields=[
                ('state_id', models.CharField(max_length=40)),
                ('month', models.DateField(help_text='Will always be YYYY-MM-01')),
                ('case_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('latest_time_end_processed', models.DateTimeField(help_text='The latest form.meta.timeEnd that has been processed for this case')),
                ('days_ration_given_mother', models.PositiveSmallIntegerField(help_text='Number of days the mother has been given rations this month', null=True)),
            ],
            options={
                'db_table': 'icds_dashboard_ccs_record_thr_forms',
            },
        ),
        migrations.CreateModel(
            name='AggregateBirthPreparednesForms',
            fields=[
                ('state_id', models.CharField(max_length=40)),
                ('month', models.DateField(help_text='Will always be YYYY-MM-01')),
                ('case_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('latest_time_end_processed', models.DateTimeField(help_text='The latest form.meta.timeEnd that has been processed for this case')),
                ('immediate_breastfeeding', models.PositiveSmallIntegerField(help_text="Has ever had /data/bp2/immediate_breastfeeding = 'yes'", null=True)),
                ('anemia', models.PositiveSmallIntegerField(help_text='Last value of /data/bp1/anemia. severe=1, moderate=2, normal=3', null=True)),
                ('eating_extra', models.PositiveSmallIntegerField(help_text="Last value of /data/bp1/eating_extra = 'yes'.", null=True)),
                ('resting', models.PositiveSmallIntegerField(help_text="Last value of /data/bp1/resting = 'yes'.", null=True)),
                ('anc_weight', models.PositiveSmallIntegerField(help_text='Last value of anc_details/anc_weight', null=True)),
                ('anc_blood_pressure', models.PositiveSmallIntegerField(help_text='Last value of anc_details/anc_blood_pressure. normal=1, high=2, not_measured=3', null=True)),
                ('bp_sys', models.PositiveSmallIntegerField(help_text='Last value of anc_details/bp_sys', null=True)),
                ('bp_dia', models.PositiveSmallIntegerField(help_text='Last value of anc_details/bp_dia', null=True)),
                ('anc_hemoglobin', models.DecimalField(decimal_places=20, help_text='Last value of anc_details/anc_hemoglobin', max_digits=64, null=True)),
                ('bleeding', models.PositiveSmallIntegerField(help_text="Last value of /data/bp2/bleeding = 'yes'", null=True)),
                ('swelling', models.PositiveSmallIntegerField(help_text="Last value of /data/bp2/swelling = 'yes'", null=True)),
                ('blurred_vision', models.PositiveSmallIntegerField(help_text="Last value of /data/bp2/blurred_vision = 'yes'", null=True)),
                ('convulsions', models.PositiveSmallIntegerField(help_text="Last value of /data/bp2/convulsions = 'yes'", null=True)),
                ('rupture', models.PositiveSmallIntegerField(help_text="Last value of /data/bp2/rupture = 'yes'", null=True)),
            ],
            options={
                'db_table': 'icds_dashboard_ccs_record_bp_forms',
            },
        ),
        migrations.CreateModel(
            name='AggregateCcsRecordDeliveryForms',
            fields=[
                ('state_id', models.CharField(max_length=40)),
                ('month', models.DateField(help_text='Will always be YYYY-MM-01')),
                ('case_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('latest_time_end_processed', models.DateTimeField(help_text='The latest form.meta.timeEnd that has been processed for this case')),
                ('breastfed_at_birth', models.PositiveSmallIntegerField(help_text='whether any child was breastfed at birth', null=True)),
            ],
            options={
                'db_table': 'icds_dashboard_ccs_record_delivery_forms',
            },
        ),
        migrations.AlterModelOptions(
            name='aggregateccsrecordpostnatalcareforms',
            options={},
        ),
        migrations.AlterModelOptions(
            name='aggregatechildhealthpostnatalcareforms',
            options={},
        ),
        migrations.AlterModelOptions(
            name='aggregatechildhealththrforms',
            options={},
        ),
        migrations.AlterModelOptions(
            name='aggregatecomplementaryfeedingforms',
            options={},
        ),
        migrations.AlterModelOptions(
            name='aggregategrowthmonitoringforms',
            options={},
        ),
    ]