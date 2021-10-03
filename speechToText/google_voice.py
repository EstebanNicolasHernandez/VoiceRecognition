from google.cloud import speech
from google.cloud import storage
import os


# Ejemplo. Traduce un audio en la nube de google relacionado al puente de Brooklyn.
def voice():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dichos-politicos.json'
    client = speech.SpeechClient()

    gcs_uri = "gs://cloud-samples-data/speech/brooklyn.flac"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Reconocimiento de voz a texto: {}".format(result.alternatives[0].transcript))


# Convierte un audio a texto.
# El audio debe tener una longitud máxima = 60 segundos
def transcribe_file(speech_file):
    client = speech.SpeechClient()

    content = speech_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        sample_rate_hertz=42000,
        enable_automatic_punctuation=True,
        language_code="es-AR",
    )

    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print("Reconocimiento de voz a texto: {}".format(result.alternatives[0].transcript))


# Convierte un audio a texto.
# Sube el archivo adjunto a un bucket de Google y retorna la URI de gsutil(La ruta de archivo del recurso en Cloud Storage).
def upload_to_bucket(attached_file, file_name):
    bucket_name = "dichos-politicos-bucket"

    storage_client = storage.Client.from_service_account_json(
        'dichos-politicos.json')

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(attached_file.name)
    blob.upload_from_filename(file_name)
    os.remove(file_name)

    return "gs://dichos-politicos-bucket/" + blob.public_url.split("/")[4]


# Debe existir en el bucket de Google el archivo.
def transcribe_gcs(gcs_uri):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        enable_automatic_punctuation=True,
        sample_rate_hertz=42000,
        language_code="es-AR",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Comenzando la traducción...")
    response = operation.result(timeout=90)
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))


def speaker_diarization():
    from google.cloud import speech_v1p1beta1 as diarization

    client = diarization.SpeechClient()

    speech_file = "resources/commercial_mono.wav"

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = diarization.RecognitionAudio(content=content)

    config = diarization.RecognitionConfig(
        encoding=diarization.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    print("Waiting for operation to complete...")
    response = client.recognize(config=config, audio=audio)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    for word_info in words_info:
        print(
            u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
        )
