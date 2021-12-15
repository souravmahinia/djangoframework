# Generated by Django 3.0.4 on 2020-04-17 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=250)),
                ('cover_pic', models.FileField(upload_to='categories/%Y/%m/%d')),
                ('description', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='contact_us',
            options={'verbose_name_plural': 'Contact Us'},
        ),
    ]