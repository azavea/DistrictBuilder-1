# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-28 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redistricting', '0010_auto_20190128_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='social_media',
            field=models.CharField(max_length=500, null=True),
        ),
    ]