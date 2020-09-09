import numpy as np
import pandas as pd
from tensorflow.keras import layers
from tensorflow.python.feature_column.feature_column_v2 import BucketizedColumn
from tensorflow.python.keras.engine.sequential import Sequential
from tensorflow.python.keras.feature_column.dense_features_v2 import DenseFeatures
import tensorflow as tf
from matplotlib import pyplot as plt
from typing import Tuple, List, Dict


def create_model(
    my_learning_rate: float,
    my_feature_layer: DenseFeatures
) -> Sequential:
    """Create and compile a simple linear regression model."""

    model = tf.keras.models.Sequential()
    # Add the layer of feature columns to the model
    model.add(my_feature_layer)

    # First hidden layer has 20 nodes and uses ReLU as its activation function
    # Include L2 Regularization at a 0.04 rate
    model.add(tf.keras.layers.Dense(
        units=20, 
        activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(0.04),
        name="Hidden1"))

    # Second hidden layer has 12 nodes and uses ReLU as its activation function
    # Include L2 Regularization at a 0.04 rate
    model.add(tf.keras.layers.Dense(
        units=12, 
        activation="relu", 
        kernel_regularizer=tf.keras.regularizers.l2(0.04),
        name="Hidden2"))

    # Define the output layer
    model.add(tf.keras.layers.Dense(
        units=1,
        name="Output"))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=my_learning_rate),
        loss="mean_squared_error",
        metrics=[tf.keras.metrics.MeanSquaredError()]
    )

    return model


def train_model(
    model: Sequential,
    dataset: pd.DataFrame,
    epochs: int,
    batch_size: int,
    label_name: str
) -> Tuple[List[int], pd.Series]:
    """Train the model by feeding it data."""

    # Map each feature name to its respective data
    features = {name: np.array(value) for name, value in dataset.items()}
    # Isolate the label data
    label = np.array(features.pop(label_name))
    
    # Train the model
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
    mse = hist["mean_squared_error"]

    return epochs, mse


def plot_the_loss_curve(
    epochs: int,
    mse: pd.Series
) -> None:
    """Plot a curve of loss vs. epoch."""

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Mean Squared Error")

    plt.plot(epochs, mse, label="Loss")
    plt.legend()
    plt.ylim([mse.min()*0.95, mse.max() * 1.03])
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
# Shuffle examples
train_df = train_df.reindex(np.random.permutation(train_df.index))
test_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_test.csv")


# Pre-process data
# ------------------------------
# Normalize the training set columns using Z-scores
train_df_mean = train_df.mean()
train_df_std = train_df.std()
train_df_norm = (train_df - train_df_mean)/train_df_std

# Normalize the test set columns using Z-scores
test_df_mean = test_df.mean()
test_df_std = test_df.std()
test_df_norm = (test_df - test_df_mean)/test_df_std


# Create feature columns
# ------------------------------
# List to hold the feature columns
feature_columns = []

# The latitude and longitude resolution should take into account their normalization
resolution_in_Zs = 0.3

# Create a bucket feature column for "latitude"
latitude = create_bucketized_column(
    train_df_norm, "latitude", resolution_in_Zs)

# Create a bucket feature column for "longitude"
longitude = create_bucketized_column(
    train_df_norm, "longitude", resolution_in_Zs)

# Create a feature cross of latitude and longitude
latitude_x_longitude = tf.feature_column.crossed_column(
    [latitude, longitude],
    hash_bucket_size=100
)
crossed_feature = tf.feature_column.indicator_column(latitude_x_longitude)
feature_columns.append(crossed_feature)

# Create a numeric column for "median_income"
median_income = tf.feature_column.numeric_column("median_income")
feature_columns.append(median_income)

# Create a numeric column for "population"
population = tf.feature_column.numeric_column("population")
feature_columns.append(population)

# Create a layer using the list of feature columns
my_feature_layer = tf.keras.layers.DenseFeatures(feature_columns)


# Set hyperparameters
# ------------------------------
learning_rate = 0.007
epochs = 140
batch_size = 1000
label_name = "median_house_value"

# Create the model
# ------------------------------
my_model = create_model(learning_rate, my_feature_layer)

# Train the model
# ------------------------------
epochs, mse = train_model(
    my_model, 
    train_df_norm, 
    epochs, 
    batch_size,
    label_name 
)
plot_the_loss_curve(epochs, mse)


# Evaluate the model
# ------------------------------
# Map each feature name to its respective data
test_features = {name:np.array(value) for name, value in test_df_norm.items()}
# Isolate the label data
test_label = np.array(test_features.pop(label_name))
my_model.evaluate(x = test_features, y = test_label, batch_size=batch_size) 