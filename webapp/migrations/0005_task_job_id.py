# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 15:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20170611_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='job_id',
            field=models.IntegerField(null=True),
        ),
    ]