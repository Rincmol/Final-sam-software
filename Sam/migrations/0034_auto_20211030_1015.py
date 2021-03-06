# Generated by Django 3.2.7 on 2021-10-30 04:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0033_auto_20211028_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name='job',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='login',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name='login',
            name='updated_at',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now, editable=False),
        ),
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateField(null=True),
        ),
    ]
