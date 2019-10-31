# Generated by Django 2.2.6 on 2019-10-31 05:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(max_length=150)),
                ('tec_head', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('tec_head_phone', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('past_exp', models.TextField()),
                ('ca_code', models.CharField(max_length=6, unique=True, verbose_name='CA Code')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='TSP_user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
