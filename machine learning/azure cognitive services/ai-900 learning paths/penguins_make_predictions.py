import os
import json
import urllib.request

endpoint = "ENDPOINT"
key = "KEY"

data = {
    "Inputs": {
        "WebServiceInput0":
        [
            {
                "CulmenLength": 49.1,
                "CulmenDepth": 4.8,
                "FlipperLength": 1220,
                "BodyMass": 5150,
            },
        ],
    },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))
headers = {
    "Content-Type": "application/json",
    "Authorization": ("Bearer " + key)
}
req = urllib.request.Request(endpoint, body, headers)

try:
    response = urllib.request.urlopen(req)
    result = response.read()
    json_result = json.loads(result)
    output = json_result["Results"]["WebServiceOutput0"][0]
    print(f"Cluster: {output['Assignments']}")

except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))
    # Print the headers to help debug
    print(error.info())
    print(json.loads(error.read().decode("utf8", "ignore")))
