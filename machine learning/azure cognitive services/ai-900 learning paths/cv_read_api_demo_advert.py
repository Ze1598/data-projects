# pip install azure-cognitiveservices-vision-computervision
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
computervision_client = ComputerVisionClient(
    cog_endpoint, 
    CognitiveServicesCredentials(cog_key)
)

# Read the image file
image_path = os.path.join("resources", "ocr", "advert.png")
image_stream = open(image_path, "rb")

# Display the image
fig = plt.figure(figsize=(7, 7))
img = Image.open(image_path)
draw = ImageDraw.Draw(img)

# Use the Computer Vision service to find text in the image
read_results = computervision_client.recognize_printed_text_in_stream(
    image_stream)

# Process the text line by line
for region in read_results.regions:
    for line in region.lines:

        # Show the position of the line of text
        l, t, w, h = list(map(int, line.bounding_box.split(",")))
        draw.rectangle(
            ( (l, t), (l+w, t+h) ), 
            outline="magenta", 
            width=1
        )

        # Read the words in the line of text
        line_text = ""
        for word in line.words:
            line_text += f"{word.text} "
        print(line_text.rstrip())

# Show the image with the text locations highlighted
plt.axis("off")
imgplot = plt.imshow(img)
plt.show()
