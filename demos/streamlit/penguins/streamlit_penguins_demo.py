import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from typing import Dict
st.set_option("deprecation.showfileUploaderEncoding", False)


@st.cache
def load_train_data() -> pd.DataFrame:
    """Load the training data without the label.
    """
    train_data = pd.read_csv("data\\penguins.csv")
    train_data.drop(["species"], axis="columns", inplace=True)
    return train_data


def create_example(input_data: Dict) -> pd.DataFrame:
    """Create a 1-example dataframe for the model prediction using the input data.
    """
    # This is 1-row dataframe, so it uses only index 0
    df = pd.DataFrame(input_data, index=[0])
    return df


st.write("""
# 🐧 Palmer Penguin Species Prediction 🐧

**Training data source**: [R palmerpenguins library by Allison Horst](https://github.com/allisonhorst/palmerpenguins)

Use the sidebar to upload a CSV with your penguin data and to create your own penguin
""")


# Create the sidebar with a file upload area for an example file and, as an\
# alternative, create input fields for all the data needed to create an example
# ------------------------------------------------
st.sidebar.header("Choose your penguin data")
st.sidebar.markdown("**Upload your penguin data as a CSV file**")

# File is uploaded as a binary buffer
uploaded_file = st.sidebar.file_uploader("", type=["csv"])

# Create the input fields
st.sidebar.markdown("**Or create your own penguin using the fields below**")
island = st.sidebar.selectbox("Island", ("Biscoe", "Dream", "Torgersen"))
sex = st.sidebar.selectbox("Gender", ("male", "female"))
# min, max, default values
bill_length_mm = st.sidebar.slider("Bill length (mm)", 32.1, 59.6, 43.9)
bill_depth_mm = st.sidebar.slider("Bill depth (mm)", 13.1, 21.5, 17.2)
flipper_length_mm = st.sidebar.slider(
    "Flipper length (mm)", 172.0, 231.0, 201.0)
body_mass_g = st.sidebar.slider("Body mass (g)", 2700.0, 6300.0, 4207.0)


# Manage the sidebar input fields' data
# ------------------------------------------------
sidebar_data = {
    "island": island,
    "bill_length_mm": bill_length_mm,
    "bill_depth_mm": bill_depth_mm,
    "flipper_length_mm": flipper_length_mm,
    "body_mass_g": body_mass_g,
    "sex": sex
}


# Create a dataframe for the latest data (sidebar input or uploaded file)
# ------------------------------------------------
st.markdown("## Current data for your example penguin")

# If a file was not uploaded, use whatever data is in the sidebar
if uploaded_file == None:
    st.write("Using sidebar data")
    # Create a dataframe for the sidebar input fields
    example_df = create_example(sidebar_data)

# If a file was uploaded use its data
elif uploaded_file != None:
    st.write("Using loaded file")
    try:
        example_df = pd.read_csv(uploaded_file)
    except:
        st.write("There was a problem loading your file.")

st.write(example_df)


# Process input data
# ------------------------------------------------
# Load the training data and append it to the example
# This way encoded features will include all the possible options
train_data = load_train_data()
complete_data = pd.concat([example_df, train_data], axis="rows")

# One-hot encode the following features
cols_to_encode = ["sex", "island"]
for column in cols_to_encode:
    one_hot_encoded = pd.get_dummies(complete_data[column], prefix=column)
    complete_data = pd.concat([complete_data, one_hot_encoded], axis="columns")
    complete_data.drop([column], axis="columns", inplace=True)

# Now that the features have been properly encoded, we only need to keep\
# the example (the first row)
processed_example = complete_data.iloc[:1]


# Load model
# ------------------------------------------------
with open("penguins_model.pkl", "rb") as f:
    model = pickle.load(f)


# Make prediction
# ------------------------------------------------
# Returns a matrix and we only need the first row
prediction = model.predict(processed_example)[0]
species = ["Adelie", "Chinstrap", "Gentoo"]
st.write(
    f"The model predicted that your penguin is of the {species[prediction]} species")
