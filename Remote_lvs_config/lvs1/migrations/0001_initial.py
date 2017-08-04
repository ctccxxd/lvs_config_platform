# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='lvsinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lvsnum', models.CharField(max_length=20, db_column=b'primaryStorageTotal')),
                ('targetIP', models.CharField(max_length=20)),
                ('VIP', models.CharField(max_length=20)),
                ('realserver', models.CharField(max_length=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='rsinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('realserver_pool', models.CharField(max_length=20)),
            ],
        ),
    ]
