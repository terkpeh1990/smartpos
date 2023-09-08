# Generated by Django 4.1.6 on 2023-09-08 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restock', '0011_historicalrestock_details_wages_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrestock',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening')], default='Morning', max_length=10),
        ),
        migrations.AddField(
            model_name='restock',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Evening', 'Evening')], default='Morning', max_length=10),
        ),
    ]