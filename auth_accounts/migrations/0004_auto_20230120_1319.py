# Generated by Django 3.1.4 on 2023-01-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_accounts', '0003_auto_20230119_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprofile',
            name='profile_code_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_code_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
