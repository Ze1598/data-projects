import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.python.keras.engine.sequential import Sequential
from matplotlib import pyplot as plt
from typing import Tuple, List, Dict

"""
This script trains a model that predicts houses' median value based solely on
the median income for houses within a block.

The model is a sequential model consisting of a single 1-neuron layer,
configured to minimize the root mean squared error during training.

The dataset used is the California Housing dataset (https://developers.google.com/machine-learning/crash-course/california-housing-data-description).
"""


def build_model(
    my_learning_rate: float
) -> Sequential:
    """Create and compile a simple linear regression model."""

    # This is a sequential model of a single 1-neuron layer
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(units=1, input_shape=(1,)))

    # Configure training to minimize the model's mean squared error
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(lr=my_learning_rate),
        loss="mean_squared_error",
        metrics=[tf.keras.metrics.RootMeanSquaredError()])

    return model


def train_model(
    model: Sequential,
    df: pd.DataFrame,
    feature: str,
    label: str,
    my_epochs: int,
    my_batch_size: int = None,
    my_validation_split: float = 0.1
) -> Tuple[List[int], pd.Series, Dict[str, List[float]]]:
    """Feed a dataset into the model in order to train it."""

    # Train the model
    history = model.fit(
        x=df[feature],
        y=df[label],
        batch_size=my_batch_size,
        epochs=my_epochs,
        validation_split=my_validation_split)

    # Get the model's trained weight and bias
    trained_weight = model.get_weights()[0]
    trained_bias = model.get_weights()[1]

    # Get the list of epochs trained on
    epochs = history.epoch

    # Get the root mean squared error for each epoch
    hist = pd.DataFrame(history.history)
    rmse = hist["root_mean_squared_error"]

    return epochs, rmse, history.history


def plot_the_loss_curve(
    epochs: List[int],
    mae_training: List[float],
    mae_validation: List[float]
) -> None:
    """Plot a curve of loss vs. epoch."""

    plt.figure()
    plt.xlabel("Epoch")
    plt.ylabel("Root Mean Squared Error")

    # Plot from the second epoch onward because the loss on the first epoch is\
    # often substantially greater than the rest
    plt.plot(epochs[1:], mae_training[1:], label="Training Loss")
    plt.plot(epochs[1:], mae_validation[1:], label="Validation Loss")
    # Add a legend
    plt.legend()

    # Calculate the combined delta of training and validation loss
    merged_mae_lists = mae_training[1:] + mae_validation[1:]
    highest_loss = max(merged_mae_lists)
    lowest_loss = min(merged_mae_lists)
    delta = highest_loss - lowest_loss

    # Set the Y axis limits
    top_of_y_axis = highest_loss + (delta * 0.05)
    bottom_of_y_axis = lowest_loss - (delta * 0.05)
    plt.ylim([bottom_of_y_axis, top_of_y_axis])

    plt.show()


# Load data
# ------------------------------
train_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv")
test_df = pd.read_csv(
    "https://download.mlcc.google.com/mledu-datasets/california_housing_test.csv")


# Data pre-processing
# ------------------------------
# Scale the "median_house_value" data on all sets
house_value_scale_factor = 1000.0
train_df["median_house_value"] /= house_value_scale_factor
test_df["median_house_value"] /= house_value_scale_factor
# Shuffle examples' order
shuffled_train_df = train_df.reindex(np.random.permutation(train_df.index))


# Set hyperparameters
# ------------------------------
learning_rate = 0.08
epochs = 70
batch_size = 100
# Percentage of examples used for the validation set
validation_split = 0.2
# Feature column (median income of a city block)
my_feature = "median_income"
# Median value of a house from a specific block
my_label = "median_house_value"


# Create the model
# ------------------------------
my_model = build_model(learning_rate)


# Train the model
# ------------------------------
epochs, rmse, history = train_model(
    my_model,
    shuffled_train_df,
    my_feature,
    my_label,
    epochs,
    batch_size,
    validation_split)

plot_the_loss_curve(
    epochs,
    history["root_mean_squared_error"],
    history["val_root_mean_squared_error"])


# Evaluate the model
# ------------------------------
# Feature data
x_test = test_df[my_feature]
# Label datas
y_test = test_df[my_label]
# Evaluate the model (outputs loss and root mean squared error)
results = my_model.evaluate(x_test, y_test, batch_size=batch_size)
