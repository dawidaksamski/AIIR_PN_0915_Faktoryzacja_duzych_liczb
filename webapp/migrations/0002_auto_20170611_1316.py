# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='job_finished_date',
            field=models.DateField(null=True),
        ),
    ]
