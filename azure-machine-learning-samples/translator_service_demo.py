import requests, uuid, json

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
cog_region = "REGION"

def translate_text(cog_region, cog_key, text, to_lang="fr", from_lang="en"):
    """
    Request a text translation from the Translation service.
    """

    # Create REST request endpoint
    path = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
    params = f"&from={from_lang}&to={to_lang}"
    api_endpoint = path + params

    # Request headers
    headers = {
        "Ocp-Apim-Subscription-Key": cog_key,
        "Ocp-Apim-Subscription-Region":cog_region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4())
    }

    # Add the text to be translated to the request body
    body = [ {"text": text} ]

    # Get the translation
    request = requests.post(api_endpoint, headers=headers, json=body)
    response = request.json()
    print(response)
    return response[0]["translations"][0]["text"]


# Translate the following text
text_to_translate = "Hello"
# To french
translation = translate_text(cog_region, cog_key, text_to_translate, to_lang="fr", from_lang="en")
print(f"{text_to_translate} -> {translation}")
# To italian
translation = translate_text(cog_region, cog_key, text_to_translate, to_lang="it-IT", from_lang="en")
print(f"{text_to_translate} -> {translation}")