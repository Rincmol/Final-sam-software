# Generated by Django 3.2.7 on 2021-11-07 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sam', '0047_rename_category_id_group_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sam.category'),
        ),
    ]