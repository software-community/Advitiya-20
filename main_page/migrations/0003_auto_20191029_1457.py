# Generated by Django 2.2.6 on 2019-10-29 09:27

from django.db import migrations, models
import main_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_auto_20191020_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main_page.models.get_file_path),
        ),
    ]
