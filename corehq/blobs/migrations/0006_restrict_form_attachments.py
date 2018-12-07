# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-26 15:11
from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import migrations

from corehq.sql_db.operations import RawSQLMigration
from corehq.sql_db.migrations import partitioned


migrator = RawSQLMigration(('corehq', 'blobs', 'sql_templates'), {})


@partitioned
class Migration(migrations.Migration):

    dependencies = [
        ('blobs', '0005_negative_id'),
    ]

    operations = [
        migrator.get_migration('restrict_legacy_attachment_metadata_insert.sql')
    ]