# pip install azure-cognitiveservices-vision-computervision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import matplotlib.pyplot as plt
from PIL import Image

cog_key = "KEY"
cog_endpoint = "ENDPOINT"

# Image to be analysed
image_path = os.path.join("resources", "store_cam1.jpg")

# Authenticate with the key
auth_instance = CognitiveServicesCredentials(cog_key)
# Get a client for the computer vision service
computervision_client = ComputerVisionClient(
    cog_endpoint,
    auth_instance
)

# Get a description from the computer vision service
image_stream = open(image_path, "rb")
response = computervision_client.describe_image_in_stream(image_stream)
tags = response.tags
captions = response.captions
first_caption = captions[0].text


def show_img_described(image_path, caption, tags):
    """
    Use PIL and Matplotlib to show the image with the caption and tags provided.
    """
    image = Image.open(image_path)
    plt.imshow(image)
    plt.axis("off")
    plt.title(f'Caption: {first_caption}\n Tags: {", ".join(tags)}')
    plt.show()


show_img_described(image_path, first_caption, tags)
