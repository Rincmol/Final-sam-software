# Generated by Django 3.2.7 on 2021-11-18 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0072_auto_20211118_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preceipt',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='preceipt',
            name='due_on',
            field=models.DateField(),
        ),
    ]
