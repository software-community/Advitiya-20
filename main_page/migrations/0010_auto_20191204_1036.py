# Generated by Django 2.2.6 on 2019-12-04 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0009_auto_20191203_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
