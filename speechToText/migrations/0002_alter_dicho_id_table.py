# Generated by Django 3.2.7 on 2021-10-01 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speechToText', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicho',
            name='id_table',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
    ]
