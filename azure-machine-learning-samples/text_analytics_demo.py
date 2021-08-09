# pip install azure-cognitiveservices-language-textanalytics
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import os

cog_key = "KEY"
cog_endpoint = "ENDPOINT"
text_analytics_client = TextAnalyticsClient(
    endpoint=cog_endpoint,
    credentials=CognitiveServicesCredentials(cog_key)
)

reviews_folder = os.path.join("resources", "reviews")
reviews_folder = os.path.join("delete")

# Create a collection of reviews with id (file name) and text (contents) properties
reviews = []
for file_name in os.listdir(reviews_folder):
    review_text = open(os.path.join(reviews_folder, file_name)).read()
    review = {"id": file_name, "text": review_text}
    reviews.append(review)

# Language detection
# -------------------------------------------------------------------------------------------------
language_analysis = text_analytics_client.detect_language(documents=reviews)

# Print the detected language for each review
for review_num in range(len(reviews)):

    lang = language_analysis.documents[review_num].detected_languages[0]
    language = lang.name
    language_code = lang.iso6391_name
    language_score = lang.score

    print(reviews[review_num]["id"])
    print(
        f" - Language: {language}\n - Code: {language_code}\n - Score: {language_score}\n")

    # Add the detected language code to the collection of reviews
    reviews[review_num]["language"] = lang.iso6391_name


# Key phrases extraction
# -------------------------------------------------------------------------------------------------
key_phrase_analysis = text_analytics_client.key_phrases(documents=reviews)

# For each review, print each key phrase found
for review_num in range(len(reviews)):
    key_phrases = key_phrase_analysis.documents[review_num].key_phrases
    
    print(reviews[review_num]["id"])
    print("\nKey Phrases:")
    [print(f"\t{key_phrase}") for key_phrase in key_phrases]
    print("\n")


# Sentiment analysis
# -------------------------------------------------------------------------------------------------
sentiment_analysis = text_analytics_client.sentiment(documents=reviews)

# Print the results for each review
for review_num in range(len(reviews)):

    # Get the sentiment score for this review
    sentiment_score = sentiment_analysis.documents[review_num].score

    # The review is negative if the score is below 0.5, positive otherwise
    if sentiment_score < 0.5:
        sentiment = "negative"
    else:
        sentiment = "positive"

    review_id = reviews[review_num]["id"]
    print(f"{review_id} : {sentiment} ({sentiment_score})")


# Extraction of known entities
# -------------------------------------------------------------------------------------------------
entity_analysis = text_analytics_client.entities(documents=reviews)

for review_num in range(len(reviews)):
    print(reviews[review_num]["id"])

    # Get the named entitites in this review
    entities = entity_analysis.documents[review_num].entities

    for entity in entities:
        # Only get datetime and location entitites
        if entity.type in ["DateTime","Location"]:
            link = f"({entity.wikipedia_url})" if entity.wikipedia_id is not None else ""
            print(f" - {entity.type}: {entity.name} {link}")