# Generated by Django 3.0.4 on 2020-05-14 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatapp', '0010_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='prperty',
            new_name='property',
        ),
    ]
