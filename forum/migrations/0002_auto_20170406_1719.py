# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 15:19
from __future__ import unicode_literals

from django.db import migrations
import draceditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_text',
            field=draceditor.models.DraceditorField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=draceditor.models.DraceditorField(),
        ),
    ]
