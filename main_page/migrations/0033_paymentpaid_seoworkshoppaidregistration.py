# Generated by Django 2.2.6 on 2020-01-23 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0032_auto_20200119_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentPaid',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_page.payment',),
        ),
        migrations.CreateModel(
            name='SEOWorkshopPaidRegistration',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_page.workshopregistration',),
        ),
    ]
