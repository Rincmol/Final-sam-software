# Generated by Django 3.2.7 on 2021-11-13 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0060_credit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preceipt',
            old_name='total2',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='receipt',
            old_name='total2',
            new_name='account',
        ),
    ]