# Generated by Django 3.0.8 on 2020-12-21 10:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20201220_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Closedbid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=64)),
                ('winner', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('winningprice', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='auctionlistings',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 21, 10, 16, 3, 409057, tzinfo=utc), max_length=64),
        ),
        migrations.AlterField(
            model_name='comments',
            name='time',
            field=models.CharField(default=datetime.datetime(2020, 12, 21, 10, 16, 3, 410252, tzinfo=utc), max_length=64),
        ),
    ]
