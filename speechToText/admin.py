from django.contrib import admin

from speechToText.models import Dicho, File

# Register your models here.

admin.site.register(File)
admin.site.register(Dicho)
