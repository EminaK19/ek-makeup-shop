# Generated by Django 3.1 on 2021-01-27 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210127_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prodused_by',
            new_name='company',
        ),
    ]
