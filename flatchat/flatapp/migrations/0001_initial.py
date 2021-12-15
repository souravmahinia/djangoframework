# Generated by Django 3.0.4 on 2020-04-13 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Us',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('contact_number', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=250)),
                ('message', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
