# Generated by Django 3.2.7 on 2021-11-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0038_alter_group_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
