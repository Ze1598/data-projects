# pip install azure.cognitiveservices.speech
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
# pip install azure-cognitiveservices-language-luis
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
import os
import requests
import json

# LUIS info
luis_app_id = "LUIS_APP_ID"
luis_key = "LUIS_KEY"
luis_endpoint = "LUIS_ENDPOINT"
# Cognitive Services info (used for Speech)
cog_key = "COGNITIVE_SERVCICES_KEY"
cog_endpoint = "COGNITIVE_SERVCICES_ENDPOINT"
cog_region = "COGNITIVE_SERVCICES_REGION"

# Authenticate into the Speech service
speech_config = SpeechConfig(cog_key, cog_region)
# Authenticate into the LUIS service
runtimeCredentials = CognitiveServicesCredentials(luis_key)
clientRuntime = LUISRuntimeClient(
    endpoint=luis_endpoint,
    credentials=runtimeCredentials
)

try:
    # Get spoken command from audio file
    file_name = "light-on.wav"
    audio_file = os.path.join("resources", "speech", file_name)

    # Configure speech recognizer
    audio_config = AudioConfig(filename=audio_file)
    speech_recognizer = SpeechRecognizer(speech_config, audio_config)

    # Use a one-time, synchronous call to transcribe the speech
    speech = speech_recognizer.recognize_once()

    # Get the predicted intent and entity
    predictionRequest = {"query": speech}

    # https://docs.microsoft.com/en-us/azure/cognitive-services/luis/client-libraries-rest-api?tabs=windows&pivots=programming-language-python
    # Get a single prediction from LUIS: intents, sentiment analysis\
    # and entities invoked
    predictionResponse = clientRuntime.prediction.get_slot_prediction(
        luis_app_id,
        "Production",
        predictionRequest
    )
    top_intent = predictionResponse.prediction.top_intent
    intents = predictionResponse.prediction.intents
    sentiment = predictionResponse.prediction.sentiment
    entities = predictionResponse.prediction.entities
    # Top intent
    print(f"Top intent: {top_intent}")
    # Intents
    print("Intents:")
    for intent in intents:
        print(f"\t{json.dumps(intent)}")
    # Sentiment analysis
    print(f"Sentiment: {sentiment}")
    # Entities invoked
    print("Entities:")
    for entity in entities:
        print(f"\t{entity}")
        print(f"\t\t{predictionResponse.prediction.entities[entity]}")


except Exception as ex:
    print(ex)
