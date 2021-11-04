from google.cloud import speech
from google.cloud import storage
import os

# Ejemplo. Traduce un audio en la nube de google relacionado al puente de Brooklyn.
from google.cloud.speech_v1 import RecognitionConfig


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


# Convierte un audio a texto. Sube el archivo adjunto a un bucket de Google y retorna
# la URI de gsutil(La ruta de archivo del recurso en Cloud Storage).
def upload_to_bucket(attached_file, file_name, is_video):
    bucket_name = "dichos-politicos-bucket"

    storage_client = storage.Client.from_service_account_json(
        'dichos-politicos.json')

    bucket = storage_client.get_bucket(bucket_name)
    if is_video:
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        os.remove(file_name)
    else:
        blob = bucket.blob(attached_file.name)
        blob.upload_from_filename(file_name)
        os.remove(attached_file.name)

    return "gs://dichos-politicos-bucket/" + blob.public_url.split("/")[4]


# Debe existir en el bucket de Google el archivo.
def transcribe_gcs(gcs_uri, interaction_type_input, device_type_input, microphone_distance):
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    metadata = speech.RecognitionMetadata()
    metadata.interaction_type = interaction_type(interaction_type_input)
    metadata.microphone_distance = mic_distance(microphone_distance)
    metadata.recording_device_type = device_type(device_type_input)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=44100,
        language_code="es-AR",
        use_enhanced=True,
        audio_channel_count=2,
        metadata=metadata,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Comenzando la traducción...")
    response = operation.result(timeout=90)
    #
    ##  for result in response.results:
        #The first alternative is the most likely one for this portion.
        #print(u"Transcript: {}".format(result.alternatives[0].transcript))
        #print("Confidence: {}".format(result.alternatives[0].confidence))
    return response


def mic_distance(microphone_distance):
    if microphone_distance == 'intermedio':
        return speech.RecognitionMetadata.MicrophoneDistance.MIDFIELD
    elif microphone_distance == 'cerca':
        return speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD
    elif microphone_distance == 'lejos':
        return speech.RecognitionMetadata.MicrophoneDistance.FARFIELD
    else:
        return speech.RecognitionMetadata.MicrophoneDistance.MICROPHONE_DISTANCE_UNSPECIFIED


def environment(environment_input):
    if environment_input == 'intermedio':
        return speech.RecognitionMetadata.MicrophoneDistance.MIDFIELD
    elif environment_input == 'cerca':
        return speech.RecognitionMetadata.MicrophoneDistance.NEARFIELD
    elif environment_input == 'lejos':
        return speech.RecognitionMetadata.MicrophoneDistance.FARFIELD
    else:
        return speech.RecognitionMetadata.MicrophoneDistance.MICROPHONE_DISTANCE_UNSPECIFIED


def device_type(device_type_input):
    if device_type_input == 'smartphone':
        return speech.RecognitionMetadata.RecordingDeviceType.SMARTPHONE
    if device_type_input == 'pc':
        return speech.RecognitionMetadata.RecordingDeviceType.PC
    if device_type_input == 'phone_line':
        return speech.RecognitionMetadata.RecordingDeviceType.PHONE_LINE
    if device_type_input == 'vehicle':
        return speech.RecognitionMetadata.RecordingDeviceType.VEHICLE
    if device_type_input == 'outdoor':
        return speech.RecognitionMetadata.RecordingDeviceType.OTHER_OUTDOOR_DEVICE
    if device_type_input == 'indoor':
        return speech.RecognitionMetadata.RecordingDeviceType.OTHER_INDOOR_DEVICE
    if device_type_input == 'unspecified':
        return speech.RecognitionMetadata.RecordingDeviceType.RECORDING_DEVICE_TYPE_UNSPECIFIED


def interaction_type(device_type_input):
    if device_type_input == 'discussion':
        return speech.RecognitionMetadata.InteractionType.DISCUSSION
    if device_type_input == 'presentation':
        return speech.RecognitionMetadata.InteractionType.PRESENTATION
    if device_type_input == 'phone_call':
        return speech.RecognitionMetadata.InteractionType.PHONE_CALL
    if device_type_input == 'voicemail':
        return speech.RecognitionMetadata.InteractionType.VOICEMAIL
    if device_type_input == 'voice_search':
        return speech.RecognitionMetadata.InteractionType.VOICE_SEARCH
    if device_type_input == 'voice_command':
        return speech.RecognitionMetadata.InteractionType.VOICE_COMMAND
    if device_type_input == 'professional':
        return speech.RecognitionMetadata.InteractionType.PROFESSIONALLY_PRODUCED
    if device_type_input == 'dictation':
        return speech.RecognitionMetadata.InteractionType.DICTATION
    if device_type_input == 'unspecified':
        return speech.RecognitionMetadata.InteractionType.INTERACTION_TYPE_UNSPECIFIED
