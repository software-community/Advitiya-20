# Generated by Django 2.2.6 on 2020-01-19 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0030_auto_20200118_0526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talk',
            name='para3',
        ),
        migrations.RemoveField(
            model_name='talk',
            name='para4',
        ),
    ]
