from typing import Tuple, List, Dict
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tensorflow.python.keras.feature_column.dense_features_v2 import DenseFeatures
from tensorflow.python.feature_column.feature_column_v2 import BucketizedColumn
from tensorflow.python.keras.engine.sequential import Sequential
from tensorflow import feature_column
from tensorflow.keras import layers
import tensorflow as tf
tf.keras.backend.set_floatx("float32")


def create_model(
    my_learning_rate: float,
    feature_layer: DenseFeatures
) -> Sequential:
    """Create and compile a simple linear regression model."""

    model = tf.keras.models.Sequential()
    # Add the layer of feature columns to the model
    model.add(feature_layer)

    # Add one linear layer to the model to yield a simple linear regressor
    model.add(tf.keras.layers.Dense(units=1, input_shape=(1,)))

    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(lr=my_learning_rate),
        loss="mean_squared_error",
        metrics=[tf.keras.metrics.RootMeanSquaredError()]
    )

    return model


def train_model(
    model: Sequential,
    dataset: pd.DataFrame,
    epochs: int,
    batch_size: int,
    label_name: str
) -> Tuple[List[int], pd.Series]:
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
        shuffle=True
    )

    # Get the list of epochs trained on
    epochs = history.epoch

    # Get the root mean squared error for each epoch
    hist = pd.DataFrame(history.history)
    rmse = hist["root_mean_squared_error"]

    return epochs, rmse


def plot_the_loss_curve(
    epochs: int,
    rmse: pd.Series
) -> None:
    """Plot a curve of loss vs. epoch."""

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Root Mean Squared Error")

    plt.plot(epochs, rmse, label="Loss")
    plt.legend()
    plt.ylim([rmse.min()*0.94, rmse.max() * 1.05])
    plt.show()


def create_bucketized_column(
    data: pd.DataFrame,
    feature: str,
    range_step: int
) -> BucketizedColumn:
    # First create a numeric column
    feature_numeric_column = tf.feature_column.numeric_column(feature)
    # Then set the buckets' range
    feature_range = list(np.arange(
        int(min(data[feature])),
        int(max(data[feature])),
        range_step
    ))
    # Finally, bucketize the numeric column based on the bucket ranges defined
    bucketized_column = tf.feature_column.bucketized_column(
        feature_numeric_column,
        feature_range
    )

    return bucketized_column


# Load data
# ------------------------------
train_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv")
test_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_test.csv")


# Pre-process data
# ------------------------------
# Scale the "median_house_value" data
scale_factor = 1000.0
train_df["median_house_value"] /= scale_factor
test_df["median_house_value"] /= scale_factor

# Shuffle examples' order
train_df = train_df.reindex(np.random.permutation(train_df.index))


# Feature engineering
# ------------------------------
# Degrees of separation of latitude/longitude for the buckets
resolution_in_degrees = 0.4
# Create a new empty list that will eventually hold the generated feature column.
feature_columns = []

# Create a bucket feature column for "latitude"
bucketized_latitude = create_bucketized_column(
    train_df,
    "latitude",
    resolution_in_degrees
)
feature_columns.append(bucketized_latitude)

# Create a bucket feature column for "longitude"
bucketized_longitude = create_bucketized_column(
    train_df,
    "longitude",
    resolution_in_degrees
)
feature_columns.append(bucketized_longitude)

# Create a feature cross of "latitude" and "longitude"
latitude_x_longitude = tf.feature_column.crossed_column(
    [bucketized_latitude, bucketized_longitude],
    hash_bucket_size=100
)
crossed_feature = tf.feature_column.indicator_column(latitude_x_longitude)
feature_columns.append(crossed_feature)

# Convert the list of feature columns into a layer that will be part of the model
feature_cross_feature_layer = layers.DenseFeatures(feature_columns)


# Set hyperparameters
# ------------------------------
learning_rate = 0.04
epochs = 35
batch_size = 100
label_name = "median_house_value"


# Create the model
# ------------------------------
my_model = create_model(learning_rate, feature_cross_feature_layer)


# Train the model
# ------------------------------
epochs, rmse = train_model(
    my_model,
    train_df,
    epochs,
    batch_size,
    label_name
)
plot_the_loss_curve(epochs, rmse)


# Evaluate the model
# ------------------------------
# Map each feature name to its respective data
test_features = {name: np.array(value) for name, value in test_df.items()}
# Isolate the label data
test_label = np.array(test_features.pop(label_name))
my_model.evaluate(x=test_features, y=test_label, batch_size=batch_size)
