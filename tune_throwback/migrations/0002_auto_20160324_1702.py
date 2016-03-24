# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tune_throwback', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rank', models.IntegerField(default=101)),
                ('week', models.DateField(default=datetime.date(1980, 1, 1))),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.TextField(default='')),
                ('artist', models.TextField(default='')),
            ],
        ),
        migrations.AddField(
            model_name='rank',
            name='song',
            field=models.ForeignKey(to='tune_throwback.Song'),
        ),
    ]
