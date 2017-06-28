# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-28 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojosecrets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokes',
            name='poked_user',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='pokes',
            name='poker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poker_id', to='dojosecrets.User'),
        ),
    ]