# Generated by Django 3.0.8 on 2020-12-21 10:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20201221_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='owner',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 21, 10, 24, 18, 431251, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 21, 10, 24, 18, 432450, tzinfo=utc), max_length=64),
        ),
    ]
