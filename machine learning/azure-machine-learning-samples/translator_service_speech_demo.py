# pip install azure.cognitiveservices.speech
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, ResultReason
from azure.cognitiveservices.speech.translation import SpeechTranslationConfig, TranslationRecognizer
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
cog_region = "REGION"
# Configure the speech translation service
translation_config = SpeechTranslationConfig(
    subscription=cog_key,
    region=cog_region
)


def translate_speech(service_instance, audio_file=None, to_lang="fr-FR", from_lang="en-US"):
    """
    Translate speech from a sound file using the Speech and Translator services.
    """
    # Specify to and from languages to use
    service_instance.speech_recognition_language = from_lang
    service_instance.add_target_language(to_lang)

    # Configure audio input
    # Use microphone as default input if no file was provided; else use a file
    if audio_file is None:
        audio_config = AudioConfig()
    else:
        audio_config = AudioConfig(filename=audio_file)

    # Create a translation recognizer and use it to translate speech input
    recognizer = TranslationRecognizer(service_instance, audio_config)
    result = recognizer.recognize_once()

    # Save the translated text and transcribed speech
    translation = ""
    speech_text = ""
    # Both were returned
    if result.reason == ResultReason.TranslatedSpeech:
        speech_text = result.text
        translation = result.translations[to_lang]
    # Only speech was returned
    elif result.reason == ResultReason.RecognizedSpeech:
        speech_text = result.text
        translation = "Unable to translate speech"
    # None were returned
    else:
        translation = "Unknown"
        speech_text = "Unknown"

    # Return the transcribed speech and translation
    return speech_text, translation

for file_name in ("english.wav", "french.wav"):
    file_path = os.path.join("resources", "speech", file_name)
    speech, translated_speech = translate_speech(
        translation_config,
        file_path,
        to_lang="es",
        from_lang="en-US"
    )

    print(f"Recognized speech: '{speech}'")
    print(f"Translation: '{translated_speech}'")
    print()
