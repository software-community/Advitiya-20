# Generated by Django 2.2.6 on 2019-11-17 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0005_participant_ca_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='name',
            field=models.CharField(default='Your Name', max_length=100),
        ),
    ]