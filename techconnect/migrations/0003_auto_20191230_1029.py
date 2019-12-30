# Generated by Django 2.2.6 on 2019-12-30 10:29

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('techconnect', '0002_centers_techconnectparticipant_workshopregistrations_workshops'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techconnectparticipant',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IN', verbose_name='Contact Number'),
        ),
    ]
