# pip install azure-cognitiveservices-vision-face
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))

# Get the ID of the first face in image 1
image_1_path = os.path.join("resources", "store_cam3.jpg")
image_1_stream = open(image_1_path, "rb")
image_1_faces = face_client.face.detect_with_stream(image=image_1_stream)
face_1 = image_1_faces[0]

# Get the face IDs in a second image
image_2_path = os.path.join("resources", "store_cam2.jpg")
image_2_stream = open(image_2_path, "rb")
image_2_faces = face_client.face.detect_with_stream(image=image_2_stream)
image_2_face_ids = list(map(lambda face: face.face_id, image_2_faces))

# Find faces in image 2 that are similar to the face in image 1
similar_faces = face_client.face.find_similar(
    face_id=face_1.face_id,
    face_ids=image_2_face_ids
)


def show_similar_faces(image_1_path, image_1_face, image_2_path, image_2_faces, similar_faces):
    """
    Based on two source images, draw bounding boxes on each face detected, identifying which ones in the second image are present in the first.
    """
    # Create a figure to display the results
    fig = plt.figure(figsize=(16, 6))

    # Show face 1
    img1 = Image.open(image_1_path)
    r = image_1_face.face_rectangle
    bounding_box = (
        (r.left, r.top),
        (r.left + r.width, r.top + r.height)
    )
    draw = ImageDraw.Draw(img1)
    draw.rectangle(bounding_box, outline="magenta", width=5)
    # The plot will be a 2x1 grid. Put the first image in the first cell
    a = fig.add_subplot(1, 2, 1)
    plt.axis("off")
    plt.imshow(img1)

    # Get the matching face IDs
    matching_face_ids = list(map(lambda face: face.face_id, similar_faces))

    # Draw a rectangle around each similar face in image 2
    img2 = Image.open(image_2_path)
    a = fig.add_subplot(1, 2, 2)
    plt.axis("off")

    for face in image_2_faces:
        r = face.face_rectangle
        bounding_box = (
            (r.left, r.top),
            (r.left + r.width, r.top + r.height)
        )

        draw = ImageDraw.Draw(img2)
        if face.face_id in matching_face_ids:
            draw.rectangle(bounding_box, outline="lightgreen", width=10)
            plt.annotate(
                "Match!",
                (r.left, r.top + r.height + 15),
                backgroundcolor="white"
            )
        else:
            draw.rectangle(bounding_box, outline="red", width=5)

    imgplot = plt.imshow(img2)
    plt.show()


show_similar_faces(
    image_1_path, face_1,
    image_2_path, image_2_faces,
    similar_faces
)
