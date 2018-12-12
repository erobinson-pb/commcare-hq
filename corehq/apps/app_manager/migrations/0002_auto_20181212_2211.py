# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-12 22:11
# flake8: noqa
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_manager', '0001_linked_app_domain'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppStream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.TextField()),
                ('build_id', models.TextField()),
                ('build_version', models.PositiveIntegerField()),
                ('stream', models.TextField(choices=[('qa', 'qa'), ('translations', 'translations'), ('development', 'development')])),
            ],
            options={
                'ordering': ('-build_version',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='appstream',
            unique_together=set([('build_id', 'stream')]),
        ),
        migrations.AlterIndexTogether(
            name='appstream',
            index_together=set([('app_id', 'build_id')]),
        ),
    ]
