# Generated by Django 3.0.8 on 2020-12-19 17:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201219_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 19, 17, 15, 37, 543716, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 19, 17, 15, 37, 544913, tzinfo=utc), max_length=64),
        ),
    ]
