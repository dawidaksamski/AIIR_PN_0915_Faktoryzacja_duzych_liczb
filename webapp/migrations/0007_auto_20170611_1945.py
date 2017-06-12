# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20170611_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='job_id',
        ),
        migrations.AddField(
            model_name='task',
            name='state',
            field=models.IntegerField(choices=[(-1, 'Cancelled'), (0, 'Waiting'), (1, 'Working'), (2, 'Done')], default=0),
        ),
    ]
