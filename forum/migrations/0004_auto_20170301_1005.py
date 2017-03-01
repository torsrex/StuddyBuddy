# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 09:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20170301_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
