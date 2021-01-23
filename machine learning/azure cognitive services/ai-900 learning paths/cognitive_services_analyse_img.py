# pip install azure-cognitiveservices-vision-computervision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
# Authenticate with the key
auth_instance = CognitiveServicesCredentials(cog_key)
# Get a client for the computer vision service
computervision_client = ComputerVisionClient(
    cog_endpoint,
    auth_instance
)

# Get the path to an image file
image_path = os.path.join("resources", "store_cam1.jpg")

# Specify the features we want to analyze
features = ['Description', 'Tags', 'Adult', 'Objects', 'Faces']

# Get an analysis from the computer vision service
image_stream = open(image_path, "rb")
analysis = computervision_client.analyze_image_in_stream(
    image_stream, visual_features=features)


def show_image_analysis(image_path, analysis):
    """
    Use PIL and Matplotlib to show the image with the caption and tags provided.
    """
    # Display the image
    fig = plt.figure(figsize=(16, 8))
    a = fig.add_subplot(1, 2, 1)
    img = Image.open(image_path)

    # Get the caption
    caption_text = ""
    if (len(analysis.description.captions) == 0):
        caption_text = "No caption detected"
    else:
        for caption in analysis.description.captions:
            caption_text = f"Caption: '{caption.text}'\n(Confidence: {caption.confidence * 100:.2f}%)"
    plt.title(caption_text)

    # Get detected objects
    if analysis.objects:
        # Draw a rectangle around each object
        for object in analysis.objects:
            r = object.rectangle
            bounding_box = (
                (r.x, r.y), 
                (r.x + r.w, r.y + r.h)
            )
            draw = ImageDraw.Draw(img)
            draw.rectangle(
                bounding_box, 
                outline="magenta", 
                width=5
            )
            plt.annotate(
                object.object_property, 
                (r.x, r.y),
                backgroundcolor="magenta"
            )

    # Get detected faces
    if analysis.faces:
        # Draw a rectangle around each face
        for face in analysis.faces:
            r = face.face_rectangle
            bounding_box = (
                (r.left, r.top),
                (r.left + r.width, r.top + r.height)
            )
            draw = ImageDraw.Draw(img)
            draw.rectangle(bounding_box, outline="lightgreen", width=5)
            annotation = f"Person aged approximately {face.age}"
            plt.annotate(
                annotation, 
                (r.left, r.top),
                backgroundcolor="lightgreen"
            )

    plt.axis("off")
    plt.imshow(img)

    # Add a second plot for addition details
    a = fig.add_subplot(1, 2, 2)

    is_adult_content = analysis.adult.is_adult_content
    is_racy_content = analysis.adult.is_racy_content
    is_gory_content = analysis.adult.is_gory_content
    # Get ratings
    ratings = f"Ratings:\n - Adult: {is_adult_content}\n - Racy: {is_racy_content}\n - Gore: {is_gory_content}"

    # Get tags
    tags = "Tags:"
    for tag in analysis.tags:
        tags = f"{tags}\n - {tag.name}"

    # Print details

    details = f"{ratings}\n\n{tags}"
    a.text(0, 0.4, details, fontsize=12)
    plt.axis("off")
    plt.show()


show_image_analysis(image_path, analysis)
