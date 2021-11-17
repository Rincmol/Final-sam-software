# Generated by Django 3.2.3 on 2021-10-25 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0017_ledger_statement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger_Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(max_length=100)),
                ('reportdate', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ledger_Masterdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(max_length=100)),
                ('reportdate', models.TextField(max_length=100)),
            ],
        ),
    ]