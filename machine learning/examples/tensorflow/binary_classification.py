import numpy as np
import pandas as pd
from tensorflow.python.keras.feature_column.dense_features_v2 import DenseFeatures
from tensorflow import feature_column
from tensorflow.keras import layers
from tensorflow.python.keras.engine.sequential import Sequential
import tensorflow as tf
from matplotlib import pyplot as plt
from typing import Tuple, List, Dict


def create_model(
    my_learning_rate: float,
    feature_layer: DenseFeatures,
    my_metrics: List
) -> Sequential:
    """Create and compile a simple classification model."""

    model = tf.keras.models.Sequential()
    # Add the layer of feature columns to the model
    model.add(feature_layer)

    # Funnel the regression value through a sigmoid function
    model.add(tf.keras.layers.Dense(
        units=1,
        input_shape=(1,),
        activation=tf.sigmoid
    ),)

    # Compile the model. Here we use BinaryCrossentropy for the loss because\
    # this is a classification model
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(lr=my_learning_rate),
        loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=my_metrics
    )

    return model


def train_model(
    model: Sequential,
    dataset: pd.DataFrame,
    epochs: int,
    label_name: str,
    batch_size: int = None,
    shuffle: bool = True
) -> Tuple[List[int], pd.DataFrame]:
    """Feed a dataset into the model in order to train it."""

    # Map each feature name to its respective data
    features = {name: np.array(value) for name, value in dataset.items()}
    # Isolate the label data
    label = np.array(features.pop(label_name))
    history = model.fit(
        x=features,
        y=label,
        batch_size=batch_size,
        epochs=epochs,
        shuffle=shuffle
    )

    # Get the list of epochs trained on
    epochs = history.epoch

    # Create a DataFrame with the loss and accuracy for each epoch
    hist = pd.DataFrame(history.history)

    return epochs, hist


def plot_curve(
    epochs: List[int],
    hist: pd.DataFrame,
    list_of_metrics: List[str]
) -> None:
    """Plot a curve of one or more classification metrics vs. epoch."""

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Value")

    # list_of_metrics should use strings as defined here:
    # https://www.tensorflow.org/tutorials/structured_data/imbalanced_data#define_the_model_and_metrics
    for m in list_of_metrics:
        x = hist[m]
        # Use only values from the second epoch onwards because the first epoch\
        # tends to have values much larger than the rest
        plt.plot(epochs[1:], x[1:], label=m)

    plt.ylim([0, 1])
    plt.legend()

    plt.show()


# Load data
# ------------------------------
train_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv")
test_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_test.csv")
# Shuffle training set
train_df = train_df.reindex(np.random.permutation(train_df.index))


# Pre-process data
# ------------------------------
# Calculate the mean and standard deviation of each feature in the\
# training set
train_df_mean = train_df.mean()
train_df_std = train_df.std()
# And normalize each value of each feature using the Z-score\
# (stored in a new DataFrame)
train_df_norm = (train_df - train_df_mean)/train_df_std

# Repeat the normalization for the test set
test_df_mean = test_df.mean()
test_df_std = test_df.std()
test_df_norm = (test_df - test_df_mean)/test_df_std

# Create a binary label "median_house_value_is_high": has a value of 1\
# if the normalized "median_house_value" value is greater than the\
# threshold (high value), otherwise it has a value of 0 (low value)
threshold_in_Z = 1.0
train_df_norm["median_house_value_is_high"] = (
    train_df_norm["median_house_value"] > threshold_in_Z).astype(float)
test_df_norm["median_house_value_is_high"] = (
    test_df_norm["median_house_value"] > threshold_in_Z).astype(float)


# Create feature columns
# ------------------------------
# List to hold feature columns
feature_columns = []

# Numerical feature column for "median_income"
median_income = tf.feature_column.numeric_column("median_income")
feature_columns.append(median_income)

# Numerical feature column for "total_rooms"
tr = tf.feature_column.numeric_column("total_rooms")
feature_columns.append(tr)

# Convert the list of feature columns into a layer that will be part of the model
feature_layer = layers.DenseFeatures(feature_columns)


# Set hyperparameters
# ------------------------------
learning_rate = 0.001
epochs = 20
batch_size = 100
classification_threshold = 0.52
label_name = "median_house_value_is_high"


# Create the model
# ------------------------------
# Define the metrics to use
METRICS = [
    tf.keras.metrics.BinaryAccuracy(
        name="accuracy",
        threshold=classification_threshold),
    tf.keras.metrics.Precision(
        thresholds=classification_threshold,
        name="precision"),
    tf.keras.metrics.Recall(name="recall")
]
# Create the model
my_model = create_model(learning_rate, feature_layer, METRICS)


# Train the model
# ------------------------------
epochs, hist = train_model(
    my_model,
    train_df_norm,
    epochs,
    label_name,
    batch_size
)

# Plot the following metrics over the epochs
list_of_metrics_to_plot = ["accuracy", "precision", "recall"]
plot_curve(epochs, hist, list_of_metrics_to_plot)


# Evaluate the model
# ------------------------------
# Map the features' names in the test set to their data
features = {name: np.array(value) for name, value in test_df_norm.items()}
# Isolate the label data
label = np.array(features.pop(label_name))
# Evaluate the model
my_model.evaluate(x=features, y=label, batch_size=batch_size)
