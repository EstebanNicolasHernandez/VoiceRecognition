from django.shortcuts import render
from django.contrib import messages

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


def audio_to_text(request):
    if request.method == 'POST':
        attached_file = request.FILES['attachInput']
        fs = FileSystemStorage()
        filename = fs.save(attached_file.name, attached_file)
        transcribe_gcs(upload_to_bucket(attached_file, fs.path(filename), False))
        print(attached_file)
    # uploaded_file_url = fs.url(filename)
    # transcribe_file(attached_file)
    # upload_to_bucket(attached_file)
    return render(request, "voz_a_texto.html")


def video_to_text(request):
    import youtube_dl
    fs = FileSystemStorage()

    if request.method == 'POST':
        video_link = request.POST['video']
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=video_link, download=False
        )
        filename = f"{video_info['title']}.mp3".replace(" ", "_")
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        messages.add_message(request, messages.INFO, "Descarga completa {}".format(filename))

        transcribe_gcs(upload_to_bucket(None, filename, True))
    return render(request, "video_a_texto.html")
