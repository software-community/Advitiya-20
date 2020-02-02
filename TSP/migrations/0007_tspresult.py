# Generated by Django 2.2.6 on 2020-02-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TSP', '0006_auto_20191208_1257'),
    ]

    operations = [
        migrations.CreateModel(
            name='TSPResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advitiya_id', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('school', models.CharField(max_length=50)),
                ('marks', models.PositiveSmallIntegerField()),
                ('rank', models.PositiveSmallIntegerField()),
            ],
        ),
    ]