"""VoiceRecognition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from speechToText.views import index, listado, acerca_de, audio_to_text, video_to_text, busqueda_dicho_politico

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acerca/', acerca_de),
    path('index/', index),
    path('listado/', listado),
    path('vozatexto/', audio_to_text, name="Voz a texto"),
    path('videoatexto/', video_to_text, name="Video a texto"),
    path('busqueda/', busqueda_dicho_politico)
]
