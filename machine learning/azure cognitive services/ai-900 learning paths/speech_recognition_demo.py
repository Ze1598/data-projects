# pip install azure.cognitiveservices.speech
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
cog_region = "REGION"
speech_config = SpeechConfig(cog_key, cog_region)

# Get spoken command from audio file
file_name = "light-on.wav"
audio_file = os.path.join("resources", "speech", file_name)

# Configure speech recognizer
# Use file instead of the default (microphone)
audio_config = AudioConfig(filename=audio_file)
# Main object to recognize speech with
speech_recognizer = SpeechRecognizer(speech_config, audio_config)

# Use a one-time, synchronous call to transcribe the speech
speech = speech_recognizer.recognize_once()
recognized_text = speech.text
print(f"Audio transcription: '{recognized_text}'")