from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from django.utils.safestring import mark_safe

from speechToText.models import Dicho
from speechToText.persistencia import insert_dicho_row, update_file_table, insert_file_row, update_dicho_table
from speechToText.google_voice import transcribe_gcs, upload_to_bucket
from django.core.files.storage import FileSystemStorage


# Create your views here.
def acerca_de(request):
    return render(request, "index.html")


def index(request):
    return render(request, "index.html")


def listado(request):
    dichos = Dicho.objects.all()
    return render(request, "listado_de_dichos.html", {"dichos": dichos})


def audio_to_text(request):
    recognized_text = ''
    if request.method == 'POST':
        device_type = request.POST['device_input']
        microphone_distance = request.POST['distance_input']
        interaction_type_input = request.POST['interaction_type_input']
        attached_file = request.FILES['attachInput']
        author = request.POST['authorInput']

        fs = FileSystemStorage()
        filename = fs.save(attached_file.name, attached_file)

        dicho_to_update = insert_dicho_row(author)
        file_to_update = insert_file_row(attached_file, dicho_to_update.file_id, False)

        gcs_uri = upload_to_bucket(attached_file, fs.path(filename), False)

        update_file_table(file_to_update, gcs_uri)

        res = transcribe_gcs(gcs_uri, interaction_type_input, device_type, microphone_distance)

        for response in res.results:
            recognized_text = recognized_text + response.alternatives[0].transcript

        update_dicho_table(dicho_to_update, recognized_text)
        messages.add_message(request, messages.INFO,
                             "Conversión finalizada. Puede buscar el texto a través del ID: " + str(
                                 dicho_to_update.id_table))
    return render(request, "voz_a_texto.html")


# Video a Texto. Primero convierte el video a mp3. Luego lo envia al bucket y lo borra del sistema,
# retornando una URI para poder convertirla a texto.
def video_to_text(request):
    global recognized_text
    import youtube_dl
    from django.core.files.base import ContentFile
    fs = FileSystemStorage()

    if request.method == 'POST':
        device_type = request.POST['device_input']
        microphone_distance = request.POST['distance_input']
        interaction_type_input = request.POST['interaction_type_input']
        author = request.POST['authorInput']
        video_link = request.POST['video']
        video_info = youtube_dl.YoutubeDL().extract_info(
            url=video_link, download=False
        )
        filename = normalize(f"{video_info['title']}.mp3".replace(" ", "_"))
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        f1 = ContentFile(filename)

        dicho_to_update = insert_dicho_row(author)
        # file_to_update = insert_file_row(f1, dicho_to_update.file_id, True)
        gcs_uri = upload_to_bucket(None, filename, True)

        # update_file_table(file_to_update, gcs_uri)
        # filename = fs.save(filename, filename)

        # messages.add_message(request, messages.INFO, "Descarga completa {}".format(filename))

        result = transcribe_gcs(gcs_uri, interaction_type_input, device_type, microphone_distance)
        for response in result.results:
            recognized_text = recognized_text + response.alternatives[0].transcript
            update_dicho_table(dicho_to_update, recognized_text)

    return render(request, "video_a_texto.html")


def busqueda_dicho_politico(request):
    global politico
    if request.method == 'POST':
        if request.POST['idInput']:
            politico = Dicho.objects.get(id_table=request.POST['idInput'])
            messages.add_message(request, messages.INFO, mark_safe(
                "<br/> <b>Autor:" + politico.author + "</b>"))
        else:
            if request.POST['authorInput'] and request.POST['fraseInput']:
                politico = Dicho.objects.get(author=request.POST['authorInput'],
                                             recognized_text=request.POST['fraseInput'])
                messages.add_message(request, messages.INFO, mark_safe(
                    "<br/> <b>Autor:" + politico.author + "</b>"))
            if request.POST['authorInput'] is not None and request.POST['fraseInput'] is None:
                politico = Dicho.objects.get(recognized_text=request.POST['fraseInput'])
                messages.add_message(request, messages.INFO, mark_safe(
                    "<br/> <b>Autor:" + politico.author + "</b>"))
            if request.POST['authorInput'] is None and request.POST[''] is not None:
                politico = Dicho.objects.get(author=request.POST['authorInput'])
                messages.add_message(request, messages.INFO, mark_safe(
                    "<br/> <b>Autor:" + politico.author + "</b>"))
            else:
                messages.error(request, "No se encontraron resultados con los filtros utilizados.")

    return render(request, "dicho_politico.html", {"politico": politico})


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b)
    return s


def dicho(request):
    if request.POST:
        politico = Dicho.objects.get(recognized_text=request.POST['fraseInput'])

    return render(request, "dicho.html", {"politico": politico})
