# Generated by Django 3.2.7 on 2021-11-08 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0050_delete_demopcash'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoPCash',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.TextField(max_length=100)),
                ('cash', models.TextField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('ledger_name', models.CharField(max_length=100)),
            ],
        ),
    ]