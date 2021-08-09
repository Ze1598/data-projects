import json
import requests
import matplotlib.pyplot as plt
from PIL import Image
import os


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
    luis_app_id = "LUIS_APP_ID"
    luis_key = "LUIS_KEY"
    luis_endpoint = "LUIS_ENDPOINT"

    # Prompt for a command
    utterance = input("Please enter a command: \n")

    # Get the predicted intent and entity
    action = get_intent(luis_app_id, luis_key, luis_endpoint, utterance)
    print(f"The action is {action}")

except Exception as ex:
    print(ex)
