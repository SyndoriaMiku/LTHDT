# Generated by Django 4.2.6 on 2023-11-09 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='produce_image/')),
                ('description', models.TextField(null=True)),
                ('category', models.CharField(choices=[('P', 'Pack'), ('C', 'Card')], max_length=5)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=50, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Order Confirm'), ('Delivered', 'Order Delivered'), ('Canceled', 'Order Cancel')], max_length=50, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.customer')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.item')),
            ],
        ),
    ]
