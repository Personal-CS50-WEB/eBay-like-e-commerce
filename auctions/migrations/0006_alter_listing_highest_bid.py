# Generated by Django 4.0.6 on 2022-09-16 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_wishlist_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='highest_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
