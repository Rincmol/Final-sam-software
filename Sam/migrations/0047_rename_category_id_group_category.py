# Generated by Django 3.2.7 on 2021-11-07 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0046_rename_category_group_category_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='category_id',
            new_name='category',
        ),
    ]