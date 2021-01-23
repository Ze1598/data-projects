# pip install azure.cognitiveservices.speech
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
cog_region = "REGION"
speech_config = SpeechConfig(cog_key, cog_region)

# Get text to be spoken
response_text = "Turning the light on."

# Configure speech synthesis
speech_config = SpeechConfig(cog_key, cog_region)
output_file = os.path.join("resources", "speech", "response.wav")
# Output speech to a file
audio_output = AudioConfig(filename=output_file)
# Output speech to speakers
# audio_output = AudioOutputConfig(use_default_speaker=True)
speech_synthesizer = SpeechSynthesizer(speech_config, audio_output)

# Transcribe text into speech
result = speech_synthesizer.speak_text(response_text)
# Play the output file using the system's default sound file player
os.system("cd resources\\speech & response.wav")