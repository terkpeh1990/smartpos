# Generated by Django 4.1.5 on 2023-01-06 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproducts',
            name='hq',
        ),
        migrations.RemoveField(
            model_name='historicalproducts',
            name='office',
        ),
        migrations.RemoveField(
            model_name='products',
            name='hq',
        ),
        migrations.RemoveField(
            model_name='products',
            name='office',
        ),
    ]