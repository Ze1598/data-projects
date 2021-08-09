# pip install azure.cognitiveservices.speech
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
import os
import requests

# LUIS info
luis_app_id = "LUIS_APP_ID"
luis_key = "LUIS_KEY"
luis_endpoint = "LUIS_ENDPOINT"
# Cognitive Services info (used for Speech)
cog_key = "COGNITIVE_SERVCICES_KEY"
cog_endpoint = "COGNITIVE_SERVCICES_ENDPOINT"
cog_region = "COGNITIVE_SERVCICES_REGION"

def get_intent(luis_app_id, cog_key, cog_endpoint, utterance):
    """
    Extract the top intent for the entities in a user utterance (command).
    """
    action = "unknown"

    try:
        print(f"Command: {utterance}")

        # Set up the REST request
        headers = dict()
        params = {
            "query": utterance,
            "subscription-key": cog_key
        }
        request_endpoint = f"{cog_endpoint}/luis/prediction/v3.0/apps/{luis_app_id}/slots/production/predict"

        # Call the LUIS app and get the prediction
        response = requests.get(
            request_endpoint,
            headers=headers,
            params=params
        )
        data = response.json()

        # Get the most probable intent
        intent = data["prediction"]["topIntent"]
        print(f"- predicted intent: {intent}")

        if intent != "None":
            # Get the target entity
            entities = data["prediction"]["entities"]
            # The original example had a "device" list of entities
            if "device" in entities:
                # Consider only the first "device" entity is identified
                device = entities["device"][0][0]
                print(f"- predicted entity: {device}")
                # Set the action to `intent_device`
                action = intent + "__" + device

        return action

    except Exception as ex:
        print(ex)
        return "unknown"

try:
    # Get spoken command from audio file
    file_name = "light-on.wav"
    audio_file = os.path.join("resources", "speech", file_name)

    # Configure speech recognizer
    speech_config = SpeechConfig(cog_key, cog_region)
    audio_config = AudioConfig(filename=audio_file)
    speech_recognizer = SpeechRecognizer(speech_config, audio_config)

    # Use a one-time, synchronous call to transcribe the speech
    speech = speech_recognizer.recognize_once()

    # Get the predicted intent and entity
    action = get_intent(luis_app_id, luis_key, luis_endpoint, speech.text)
    print(f"The action is {action}")

except Exception as ex:
    print(ex)