# Generated by Django 2.2.6 on 2019-12-27 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0021_workshop_workshop_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopPaidRegistration',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main_page.workshopregistration',),
        ),
        migrations.AddField(
            model_name='workshop',
            name='at_sudhir',
            field=models.BooleanField(default=False),
        ),
    ]