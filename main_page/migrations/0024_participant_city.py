# Generated by Django 2.2.6 on 2019-12-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0023_auto_20191227_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='city',
            field=models.CharField(default='none', max_length=50),
            preserve_default=False,
        ),
    ]