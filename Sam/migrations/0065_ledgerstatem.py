# Generated by Django 3.2.7 on 2021-11-15 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0064_delete_ledgerstatem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ledgerStatem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From_Date', models.DateField()),
                ('To_Date', models.DateField()),
                ('Ledger_Name', models.CharField(max_length=50)),
            ],
        ),
    ]
