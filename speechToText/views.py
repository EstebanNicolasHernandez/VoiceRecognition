from django.shortcuts import render
from speechToText.models import Dicho
from google.cloud import speech
import os


# Create your views here.
def acerca_de(request):
    return render(request, "acercade.html")


def contact(request):
    return render(request, "contacto.html")


def index(request):
    return render(request, "index.html")


def listado(request):
    dichos = Dicho.objects.all()

    return render(request, "listadoDeDichos.html", {"dichos": dichos})


def voz_a_texto(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['attachInput']

        print(uploaded_file)
    return render(request, "vozATexto.html")


def google_api():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dichos-politicos.json'
    client = speech.SpeechClient()

    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Reconocimiento de voz a texto: {}".format(result.alternatives[0].transcript))
