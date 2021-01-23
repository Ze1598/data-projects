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
image_path = os.path.join("resources", "store_cam1.jpg")
image_stream = open(image_path, "rb")

# Detect faces and specified facial attributes
attributes = ["age", "emotion"]
detected_faces = face_client.face.detect_with_stream(image=image_stream, return_face_attributes=attributes)

def show_face_attributes(image_path, detected_faces):
    """
    Draw bounding boxes for each detected face, and the analysed attributes.
    """
    # Open an image
    img = Image.open(image_path)

    # Create a figure to display the results
    fig = plt.figure(figsize=(8, 6))

    if detected_faces:

        num_faces = len(detected_faces)
        prediction = f"({str(num_faces)} faces detected)"

        # Draw the bounding box
        for face in detected_faces:
            r = face.face_rectangle
            bounding_box = (
                (r.left, r.top), 
                (r.left + r.width, r.top + r.height)
            )

            draw = ImageDraw.Draw(img)
            draw.rectangle(bounding_box, outline="magenta", width=5)

            # Get the attributes as a dictionary
            detected_attributes = face.face_attributes.as_dict()
            
            # Process the age
            age = "age unknown" if "age" not in detected_attributes.keys() else int(detected_attributes["age"])
            annotations = f"Person aged approximately {age}"
            
            # Process the emotions
            txt_lines = 1
            if "emotion" in detected_attributes.keys():
                for emotion_name in detected_attributes["emotion"]:
                    txt_lines += 1
                    emotion_value = detected_attributes["emotion"][emotion_name]
                    annotations += f"\n - {emotion_name}: {emotion_value}"
            
            # Annotate with the analysis
            plt.annotate(
                annotations,
                (
                    (r.left + r.width), 
                    (r.top + r.height + (txt_lines * 12))
                ), 
                backgroundcolor="white"
            )

        # Plot the image
        fig.suptitle(prediction)

    plt.axis("off")
    imgplot = plt.imshow(img)
    plt.show()

show_face_attributes(image_path, detected_faces)