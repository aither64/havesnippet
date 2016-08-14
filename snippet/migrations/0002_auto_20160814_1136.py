# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='downloads',
            field=models.PositiveIntegerField(default=0, verbose_name='downloads'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='embed_views',
            field=models.PositiveIntegerField(default=0, verbose_name='embed views'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='raw_views',
            field=models.PositiveIntegerField(default=0, verbose_name='raw views'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='views'),
        ),
    ]