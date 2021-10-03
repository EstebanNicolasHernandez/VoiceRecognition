from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from speechToText.models import Dicho
from speechToText.google_voice import transcribe_file, transcribe_gcs, upload_to_bucket
from django.core.files.storage import FileSystemStorage

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
        attached_file = request.FILES['attachInput']
        fs = FileSystemStorage()
        filename = fs.save(attached_file.name, attached_file)
        uploaded_file_url = fs.url(filename)
        # transcribe_file(attached_file)
        # upload_to_bucket(attached_file)
        transcribe_gcs(upload_to_bucket(attached_file,fs.path(filename)))
        print(attached_file)
    return render(request, "voz_a_texto.html")
