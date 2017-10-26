# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demosky', '0004_sensors'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='birthplace',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='quote',
            field=models.TextField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='study',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='work',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(default='', max_length=500),
        ),
    ]
