# Generated by Django 3.1.4 on 2021-03-21 07:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210321_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='auction',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]