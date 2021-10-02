from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from speechToText.models import Dicho
from speechToText.google_voice import transcribe_file, transcribe_gcs,upload_to_bucket


# Create your views here.
def acerca_de(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contacto.html")


def index(request):
    return render(request, "index.html")


def listado(request):
    dichos = Dicho.objects.all()

    return render(request, "listado_de_dichos.html", {"dichos": dichos})


def voz_a_texto(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['attachInput']
      #  transcribe_file(uploaded_file)
        transcribe_gcs("gs://dichos-politicos-bucket/las-frases-mas-polemicas-de-alberto-fernandez.mp3")
        print(uploaded_file)
    return render(request, "voz_a_texto.html")

