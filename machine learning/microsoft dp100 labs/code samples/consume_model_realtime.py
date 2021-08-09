import json
import requests

# WebService object that references your model service
service = ...


# Consume the service through the SDK
###############################################################################
# An array of new data cases
x_new = [
    [0.1, 2.3, 4.1, 2.0],
    [0.2, 1.8, 3.9, 2.1]
]

# Convert the array to a serializable list in a JSON document
json_data = json.dumps({"data": x_new})

# Call the web service, passing the input data
response = service.run(input_data=json_data)

# Get the predictions
predictions = json.loads(response)

# Print the predicted class for each case.
for i in range(len(x_new)):
    print(x_new[i], predictions[i])
###############################################################################


# Consume the service through REST endpoint (anonymous)
###############################################################################
endpoint = service.scoring_uri
print(endpoint)


# An array of new data cases
x_new = [
    [0.1, 2.3, 4.1, 2.0],
    [0.2, 1.8, 3.9, 2.1]
]

# Convert the array to a serializable list in a JSON document
json_data = json.dumps({"data": x_new})

# Set the content type in the request headers
request_headers = {"Content-Type": "application/json"}

# Call the service
response = requests.post(
    url=endpoint,
    data=json_data,
    headers=request_headers
)

# Get the predictions from the JSON response
predictions = json.loads(response.json())

# Print the predicted class for each case.
for i in range(len(x_new)):
    print(x_new[i], predictions[i])
###############################################################################


# Consume the service through REST endpoint (authenticated)
###############################################################################
# Auth is disabled for ACI services by default
# Key-based auth is default for AKS services
# AKS can be configured to use token-based authentication (not supported for ACI)

# Get auth keys (assuming there is an active authenticated AML session)
primary_key, secondary_key = service.get_keys()

# An array of new data cases
x_new = [
    [0.1, 2.3, 4.1, 2.0],
    [0.2, 1.8, 3.9, 2.1]
]

# Convert the array to a serializable list in a JSON document
json_data = json.dumps({"data": x_new})

# Set the content type in the request headers
request_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key_or_token}"
}

# Call the service
response = requests.post(
    url=endpoint,
    data=json_data,
    headers=request_headers
)

# Get the predictions from the JSON response
predictions = json.loads(response.json())

# Print the predicted class for each case.
for i in range(len(x_new)):
    print(x_new[i], predictions[i])
###############################################################################
