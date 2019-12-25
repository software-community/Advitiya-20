# Generated by Django 2.2.6 on 2019-12-25 16:20

from django.db import migrations, models
import main_page.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0018_workshopregistration_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workshopregistration',
            name='image',
        ),
        migrations.AddField(
            model_name='workshop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=main_page.models.get_file_path),
        ),
    ]