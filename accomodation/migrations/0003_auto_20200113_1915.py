# Generated by Django 2.2.6 on 2020-01-13 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accomodation', '0002_auto_20200113_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]