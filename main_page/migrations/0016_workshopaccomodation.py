# Generated by Django 2.2.6 on 2019-12-25 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0015_auto_20191224_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkshopAccomodation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accomodation_on_7th', models.BooleanField(default=False)),
                ('accomodation_on_8th', models.BooleanField(default=False)),
                ('accomodation_on_9th', models.BooleanField(default=False)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
        ),
    ]
