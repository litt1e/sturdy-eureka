# Generated by Django 2.2.1 on 2019-05-20 09:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20190520_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='short_title',
            field=models.CharField(default='thre', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 20, 12, 34, 9, 881569)),
        ),
        migrations.AlterField(
            model_name='thread',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 20, 12, 34, 9, 881569)),
        ),
    ]
