# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-13 15:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=40, unique=True)),
                ('description', models.CharField(max_length=100, verbose_name='description')),
                ('use_count', models.IntegerField(default=0, verbose_name='use count')),
                ('last_use', models.DateTimeField(blank=True, null=True, verbose_name='last use')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
