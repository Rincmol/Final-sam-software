# Generated by Django 3.2.7 on 2021-11-07 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0045_alter_group_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='category',
            new_name='category_id',
        ),
    ]
