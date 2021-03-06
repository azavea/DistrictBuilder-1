# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-18 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redistricting', '0007_auto_20181018_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contest_division',
            field=models.CharField(choices=[(b'ADULT', b'Adult (non-student)'), (b'YOUTH', b'Youth (Age 13 through Grade 12)'), (b'ACADM', b'Higher Ed (Undergraduate, graduate, professional')], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='county',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
