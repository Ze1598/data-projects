# >> streamlit run streamlit_iris_demo.py
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Global variables
# ---------------------------------------------------------------
# Possible classes/flower types (ordered as in the dataset)
CLASSES = ["Setosa", "Versicolor", "Virginica"]


def user_input_features():
    """Create a 1-row dataframe to simulate a flower based on the user input.
    """
    # Create sliders for various input values
    sepal_length = st.sidebar.slider("Sepal length", 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider("Sepal width", 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider("Petal length", 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider("Petal width", 0.1, 2.5, 0.2)

    # Organize the data in a dictionary
    data = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }
    # And create a dataframe for it
    features = pd.DataFrame(data, index=[0])

    return features


st.write("# Iris Flower Prediction")
st.sidebar.header("User Input Parameters")


# Process the input data
# ---------------------------------------------------------------
# Create a dataframe of 1 flower based on the user's input
df = user_input_features()
st.subheader("User Input parameters")
# Display the input data
st.write(df)


# Load the iris dataset
# ---------------------------------------------------------------
iris = datasets.load_iris()
# Separate the features and the label
X = iris.data
Y = iris.target


# Model creation, training and prediction
# ---------------------------------------------------------------
# Create a Random Forest Classifier model
model = RandomForestClassifier()
# Train the model
model.fit(X, Y)
# Make a prediction for the input flower data (returns a matrix)
prediction = model.predict(df)[0]


# Show the model prediction
# ---------------------------------------------------------------
st.subheader("Prediction")
st.write(
    f"The model predicted your flower is of the type *{CLASSES[prediction]}*")


# Show the class probabilities
# ---------------------------------------------------------------
st.subheader("Prediction Probabilities")
# Get a matrix with the probabilities of each class (it has a single row)
prediction_prob = model.predict_proba(df)[0]
# Pair each class to its predicted probability
prob_by_class = zip(CLASSES, prediction_prob)
prob_df = pd.DataFrame(
    data=prob_by_class,
    columns=["Flower Type", "Predicted Probability"]
)
st.write(prob_df)
