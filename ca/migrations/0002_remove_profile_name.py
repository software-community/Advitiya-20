# Generated by Django 2.2.6 on 2019-10-08 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]
