# pip install azure-cognitiveservices-vision-customvision
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

project_id = "PROJECT_ID"
cv_key = "KEY"
cv_endpoint = "ENDPOINT"
model_name = "MODEL_NAME"

# Load a test image and get its dimensions
test_img_file = os.path.join("some_path")
test_img = Image.open(test_img_file)
test_img_h, test_img_w, test_img_ch = np.array(test_img).shape

# Get a prediction client for the object detection model
credentials = ApiKeyCredentials(in_headers={"Prediction-key": cv_key})
predictor = CustomVisionPredictionClient(
    endpoint=cv_endpoint,
    credentials=credentials
)

print(
    f"Detecting objects in {test_img_file} using model {model_name} in project {project_id}...")

# Detect objects in the test image
with open(test_img_file, mode="rb") as test_data:
    results = predictor.detect_image(project_id, model_name, test_data)

# Create a figure to display the results
fig = plt.figure(figsize=(8, 8))
plt.axis("off")

# Display the image with boxes around each detected object
draw = ImageDraw.Draw(test_img)
line_width = int(np.array(test_img).shape[1] / 100)
object_colors = {
    "apple": "lightgreen",
    "banana": "yellow",
    "orange": "orange"
}
for prediction in results.predictions:
    # Default color for any other object tags
    color = "white"

    if (prediction.probability * 100) > 50:

        # Update the color if the model detected an expected object
        if prediction.tag_name in object_colors:
            color = object_colors[prediction.tag_name]

        # Calculate the length for each side of the bounding box
        left = prediction.bounding_box.left * test_img_w
        top = prediction.bounding_box.top * test_img_h
        height = prediction.bounding_box.height * test_img_h
        width = prediction.bounding_box.width * test_img_w
        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)
        )

        # Draw the complete box
        draw.line(points, fill=color, width=line_width)
        # And add the tag to the box
        tag_text = f"{prediction.tag_name}: {prediction.probability * 100:.2f}%"
        plt.annotate(tag_text, (left, top), backgroundcolor=color)

imgplot = plt.imshow(test_img)
plt.show()
