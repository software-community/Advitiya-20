# Generated by Django 2.2.6 on 2019-10-20 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'Aeromodelling'), ('2', 'Finance'), ('3', 'Coding'), ('4', 'Robotics'), ('5', 'Automotive'), ('6', 'CAD'), ('7', 'Astronomy'), ('8', 'Gaming'), ('9', 'Quizzing'), ('10', 'Entrepreneurship'), ('11', 'Photo Editing')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('venue', models.CharField(max_length=100)),
                ('team_lower_limit', models.IntegerField()),
                ('team_upper_limit', models.IntegerField()),
                ('fees', models.IntegerField()),
                ('prize', models.IntegerField()),
                ('rulebook', models.URLField()),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField()),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Coordinator')),
            ],
        ),
    ]