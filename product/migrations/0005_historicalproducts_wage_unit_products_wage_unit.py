# Generated by Django 4.1.6 on 2023-09-08 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_id_alter_historicalcategory_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproducts',
            name='wage_unit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='products',
            name='wage_unit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
