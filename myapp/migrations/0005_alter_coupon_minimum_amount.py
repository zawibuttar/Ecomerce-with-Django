# Generated by Django 5.0.3 on 2024-06-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='minimum_amount',
            field=models.IntegerField(default=1000),
        ),
    ]
