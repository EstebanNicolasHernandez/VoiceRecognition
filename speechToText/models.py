from django.db import models


# Create your models here.
class Dicho(models.Model):
    id_table = models.AutoField(primary_key=True, unique=True)
    file_id = models.IntegerField(null=True)
    author = models.CharField(max_length=50)
    url = models.CharField(max_length=200, null=True)
    recognized_text = models.CharField(max_length=6000)


class File(models.Model):
    id_file = models.AutoField(primary_key=True, unique=True)
    file_type = models.CharField(max_length=15)
    file_attached = models.BinaryField(null=True)
    file_uri = models.CharField(null=True, max_length=500)

# Crear tabla metadata
