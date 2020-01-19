# Generated by Django 2.2.6 on 2020-01-19 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0032_auto_20200119_2214'),
        ('startup_conclave', '0002_bootcampregistrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentForStalls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_request_id', models.CharField(default='none', max_length=100)),
                ('transaction_id', models.CharField(default='none', max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
        ),
    ]
