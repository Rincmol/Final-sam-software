# Generated by Django 3.2.7 on 2021-09-16 07:41

import Sam.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.TextField(max_length=100)),
                ('item_desc', models.TextField(max_length=500, null=True)),
                ('item_barcode', models.TextField(max_length=50)),
                ('item_category', models.TextField(max_length=50)),
                ('item_unit_prim', models.TextField(max_length=100)),
                ('item_unit_sec', models.TextField(max_length=100)),
                ('open_balance', models.TextField(max_length=100)),
                ('buying_price', models.TextField(max_length=50)),
                ('sell_price', models.TextField(max_length=50)),
                ('image1', models.ImageField(blank=True, null=True, upload_to=Sam.models.filepath)),
                ('image2', models.ImageField(blank=True, null=True, upload_to=Sam.models.filepath)),
                ('image3', models.ImageField(blank=True, null=True, upload_to=Sam.models.filepath)),
                ('image4', models.ImageField(blank=True, null=True, upload_to=Sam.models.filepath)),
            ],
        ),
    ]
