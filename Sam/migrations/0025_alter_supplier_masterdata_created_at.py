# Generated by Django 3.2.7 on 2021-10-26 11:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0024_alter_supplier_masterdata_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier_masterdata',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, editable=False),
        ),
    ]