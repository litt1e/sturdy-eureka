# Generated by Django 2.2.1 on 2019-05-31 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20190520_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.CharField(default='AnonymousUser', max_length=20),
        ),
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.CharField(default='AnonymousUser', max_length=20),
        ),
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 31, 15, 32, 54, 763645)),
        ),
        migrations.AlterField(
            model_name='thread',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 31, 15, 32, 54, 763645)),
        ),
    ]