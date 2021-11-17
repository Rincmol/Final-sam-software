# Generated by Django 3.2.7 on 2021-10-26 12:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0027_auto_20211026_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier_masterdata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='supplier_masterdata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
