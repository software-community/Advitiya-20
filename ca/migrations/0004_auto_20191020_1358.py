# Generated by Django 2.2.6 on 2019-10-20 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ca', '0003_profile_why_ca'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='why_ca',
        ),
        migrations.AddField(
            model_name='profile',
            name='past_exp',
            field=models.TextField(default='r'),
            preserve_default=False,
        ),
    ]
