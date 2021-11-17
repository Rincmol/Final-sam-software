# Generated by Django 3.2.3 on 2021-10-25 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0016_auto_20211019_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ledger_Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.TextField(max_length=100)),
                ('ledger_name', models.TextField(max_length=100)),
                ('ledger_id', models.TextField(max_length=100)),
                ('period', models.TextField(max_length=100)),
            ],
        ),
    ]