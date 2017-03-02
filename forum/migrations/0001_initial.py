# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 10:11
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
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('answer_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('answer_updated', models.DateTimeField(auto_now_add=True, verbose_name='Date updated')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=60)),
                ('question_text', models.TextField()),
                ('question_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('question_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('question_SuitableForQuiz', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=60)),
                ('topic_desc', models.CharField(max_length=200)),
                ('topic_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('topic_updated', models.DateTimeField(auto_now_add=True, verbose_name='Date updated')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='forum.Topic'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='forum.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Topic'),
        ),
    ]
