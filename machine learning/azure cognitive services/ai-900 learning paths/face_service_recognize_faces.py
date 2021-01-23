# pip install azure-cognitiveservices-vision-face
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
face_client = FaceClient(cog_endpoint, CognitiveServicesCredentials(cog_key))


# Create a new group of people. If it exists already, delete it first
group_id = "employee_group_id"
try:
    face_client.person_group.delete(group_id)
except Exception as ex:
    print(ex.message)
finally:
    face_client.person_group.create(group_id, "employees")
    print("Group created!")


# Add a person to the group
wendell = face_client.person_group_person.create(group_id, "Wendell")

# Get training photos for the person
folder = os.path.join("resources", "wendell")
wendell_pics = os.listdir(folder)

# Register the photos in the group
i = 0
fig = plt.figure(figsize=(8, 8))
for pic in wendell_pics:
    # Load the photos as a stream
    img_path = os.path.join(folder, pic)
    img_stream = open(img_path, "rb")
    # And register the photos specifically for Wendell, not other members of the group
    face_client.person_group_person.add_face_from_stream(
        group_id,
        wendell.person_id,
        img_stream
    )

    # Display each photo in a grid
    img = Image.open(img_path)
    i += 1
    _ = fig.add_subplot(1, len(wendell_pics), i)
    _.axis("off")
    imgplot = plt.imshow(img)

# Show the training photos side by side
plt.show()
# Train the model to recognize Wendell using the photos loaded
face_client.person_group.train(group_id)
print("Trained!")

# Get the face IDs for everyone in a second image
image_path = os.path.join("resources", "employees.jpg")
image_stream = open(image_path, "rb")
image_faces = face_client.face.detect_with_stream(image=image_stream)
image_face_ids = list(map(lambda face: face.face_id, image_faces))

# Get recognized face names
face_names = {}
# Looking for everyone in the group, not just Wendell
recognized_faces = face_client.face.identify(image_face_ids, group_id)
for face in recognized_faces:
    person_id_detected = face.candidates[0].person_id
    person_name = face_client.person_group_person.get(
        group_id,
        person_id_detected
    ).name
    face_names[face.face_id] = person_name


def show_recognized_faces(image_path, detected_faces, recognized_face_names):
    """
    Draw bounding boxes for faces of recognized people in a photo.
    """
    # Open an image
    img = Image.open(image_path)

    # Create a figure to display the results
    fig = plt.figure(figsize=(8, 6))

    if detected_faces:
        num_faces = len(recognized_face_names)
        caption = f"({str(num_faces)} faces recognized)"

        # Draw a rectangle around each detected face
        for face in detected_faces:
            r = face.face_rectangle
            bounding_box = (
                (r.left, r.top),
                (r.left + r.width, r.top + r.height)
            )

            draw = ImageDraw.Draw(img)
            draw.rectangle(bounding_box, outline="magenta", width=5)

            # The bounding box is drawn for all detected faces, but they\
            # only have a name if they were recognized
            if face.face_id in recognized_face_names:
                plt.annotate(
                    recognized_face_names[face.face_id],
                    (r.left, r.top + r.height + 15),
                    backgroundcolor="white"
                )

        fig.suptitle(caption)

    plt.axis("off")
    imgplot = plt.imshow(img)
    plt.show()


show_recognized_faces(image_path, image_faces, face_names)
