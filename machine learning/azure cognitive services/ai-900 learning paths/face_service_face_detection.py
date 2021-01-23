# pip install azure-cognitiveservices-vision-face
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# Open an image
image_path = os.path.join("resources", "store_cam2.jpg")
image_stream = open(image_path, "rb")

# Detect faces
detected_faces = face_client.face.detect_with_stream(image=image_stream)


def show_faces(image_path, detected_faces, show_id=False):
    """
    Draw bounding boxes for each face detected, and the face id if specified.
    """
    img = Image.open(image_path)
    fig = plt.figure(figsize=(8, 6))

    num_faces = len(detected_faces)
    prediction = f"({str(num_faces)} faces detected)"

    # Draw the faces' bounding boxex
    for face in detected_faces:
        r = face.face_rectangle
        # Calculate the four box coordinates
        bounding_box = (
            (r.left, r.top),
            (r.left + r.width, r.top + r.height)
        )

        draw = ImageDraw.Draw(img)
        draw.rectangle(bounding_box, outline="magenta", width=5)

        # Only show the face id if required
        if show_id:
            plt.annotate(
                face.face_id, 
                (r.left, r.top + r.height + 15), 
                backgroundcolor="white"
            )

    fig.suptitle(prediction)
    plt.axis("off")
    imgplot = plt.imshow(img)
    plt.show()

show_faces(image_path, detected_faces)