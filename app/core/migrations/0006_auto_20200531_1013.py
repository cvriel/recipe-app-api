# Generated by Django 2.1.15 on 2020-05-31 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_miniutes',
            new_name='time_minutes',
        ),
    ]
