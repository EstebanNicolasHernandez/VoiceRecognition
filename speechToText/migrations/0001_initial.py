# Generated by Django 3.2.7 on 2021-10-01 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dicho',
            fields=[
                ('id_table', models.IntegerField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=50)),
                ('recognized_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id_file', models.IntegerField(primary_key=True, serialize=False)),
                ('file_type', models.CharField(max_length=15)),
            ],
        ),
    ]