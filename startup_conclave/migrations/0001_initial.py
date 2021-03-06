# Generated by Django 2.2.6 on 2020-01-19 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_page', '0031_auto_20200119_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartupTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Team Name')),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
        ),
        migrations.CreateModel(
            name='StartupTeamHasMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='startup_conclave.StartupTeam')),
            ],
        ),
        migrations.CreateModel(
            name='StartupRegistrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.Participant')),
            ],
        ),
    ]
