from google.cloud import speech
from google.cloud import storage
import os


# Ejemplo. Traduce un audio en la nube de google relacionado al puente de Brooklyn.
def voice(file):
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


# Recibe un file de la vista voz_a_texto.html para poder ser convertido a texto.
def transcribe_file(speech_file):
    client = speech.SpeechClient()

    content = speech_file.read()

   # audio = speech.RecognitionAudio(content=content)
   # config = speech.RecognitionConfig(
    #    sample_rate_hertz=48000,
     #  language_code="es-AR",
    #)

   # response = client.recognize(config=config, audio=audio)

    #print(response)


#    for result in response.results:
#       print(u"Transcript: {}".format(result.alternatives[0].transcript))

#Método para reconocer audios que duren más de 60 segundos.
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        sample_rate_hertz=42000,
        language_code="es-AR",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)
    print(response)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    # for result in response.results:
        # The first alternative is the most likely one for this portion.
    #    print(u"Transcript: {}".format(result.alternatives[0].transcript))
    #   print("Confidence: {}".format(result.alternatives[0].confidence))

#def upload_to_bucket(blob_name, path_to_file, bucket_name):
def upload_to_bucket():
    """ Upload data to a bucket"""

    blob_name,path_to_file,bucket_name = ""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'dichos-politicos.json')

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    # returns a public url
    return blob.public_url
