from django.db import models


# Create your models here.
class Dicho(models.Model):
    id_table = models.IntegerField(primary_key=True, unique=True)
    id_file = models.IntegerField(null=True)
    author = models.CharField(max_length=50)
    recognized_text = models.CharField(max_length=100)


class File(models.Model):
    id_file = models.IntegerField(primary_key=True)
    file_type = models.CharField(max_length=15)
