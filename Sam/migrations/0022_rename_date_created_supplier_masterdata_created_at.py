# Generated by Django 3.2.7 on 2021-10-26 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0021_supplier_masterdata_date_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier_masterdata',
            old_name='date_created',
            new_name='created_at',
        ),
    ]
