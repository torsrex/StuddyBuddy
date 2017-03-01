# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 09:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20170301_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL),
        ),
    ]
