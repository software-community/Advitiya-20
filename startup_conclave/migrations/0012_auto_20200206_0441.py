# Generated by Django 2.2.6 on 2020-02-06 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup_conclave', '0011_auto_20200126_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startupteam',
            name='cin_no',
            field=models.CharField(blank=True, max_length=21, null=True, verbose_name='Corporate Identification Number (CIN Number)'),
        ),
    ]
