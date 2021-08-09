# pip install azure-cognitiveservices-vision-computervision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image
import time
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
computervision_client = ComputerVisionClient(
    cog_endpoint,
    CognitiveServicesCredentials(cog_key)
)

# Read the image file
# Computer text
image_path = os.path.join("resources", "ocr", "letter.jpg")
# Hand-written text
# image_path = os.path.join("resources", "ocr", "note.jpg")
image_stream = open(image_path, "rb")

# Get a client for the computer vision service
computervision_client = ComputerVisionClient(
    cog_endpoint,
    CognitiveServicesCredentials(cog_key)
)

# Submit a request to read printed text in the image and get the operation ID
read_operation = computervision_client.read_in_stream(
    image_stream,
    raw=True
)
operation_location = read_operation.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

# Wait for the asynchronous operation to complete
while True:
    read_results = computervision_client.get_read_result(operation_id)
    if read_results.status not in [OperationStatusCodes.running]:
        break
    time.sleep(1)

# If the operation was successful, process the text line by line
if read_results.status == OperationStatusCodes.succeeded:
    for result in read_results.analyze_result.read_results:
        for line in result.lines:
            print(line.text)

# Open image and display it
print("\n")
fig = plt.figure(figsize=(12, 12))
img = Image.open(image_path)
plt.axis("off")
imgplot = plt.imshow(img)
plt.show()
