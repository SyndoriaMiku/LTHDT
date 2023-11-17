# Generated by Django 4.2.6 on 2023-11-16 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_orders_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.PositiveBigIntegerField(),
        ),
    ]
