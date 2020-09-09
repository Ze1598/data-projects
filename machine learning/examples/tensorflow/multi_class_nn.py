import numpy as np
import pandas as pd
from tensorflow.keras import layers
from tensorflow.python.keras.engine.sequential import Sequential
from tensorflow.python.keras.feature_column.dense_features_v2 import DenseFeatures
import tensorflow as tf
from matplotlib import pyplot as plt
from typing import Tuple, List, Dict


def create_model(
    my_learning_rate: float
) -> Sequential:
    """Create and compile a deep neural net."""

    model = tf.keras.models.Sequential()
    # Features are represented as a 28x28 array of color values
    # Flatten them into 784x1 arrays
    model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))

    # Define the first hidden layer
    model.add(tf.keras.layers.Dense(
        units=256,
        activation="relu"
    ))

    # Define a dropout regularization layer after the first hidden layer
    model.add(tf.keras.layers.Dropout(rate=0.2))
    
    # Define the second hidden layer
    model.add(tf.keras.layers.Dense(
        units=128,
        activation="relu"
    ))

    # Define the output layer
    # The model must predict one of ten possible digits, thus the output\
    # layer has 10 nodes
    model.add(tf.keras.layers.Dense(
        units=10,
        activation="softmax"
    ))

    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=my_learning_rate),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def train_model(
    model: Sequential, 
    train_features: pd.DataFrame, 
    train_label: str, 
    epochs: int,
    batch_size: int = None, 
    validation_split: float = 0.1
) -> Tuple[List[int], pd.Series]:
    """Train the model by feeding it data."""

    history = model.fit(
        x=train_features, 
        y=train_label, 
        batch_size=batch_size,
        epochs=epochs, 
        shuffle=True,
        validation_split=validation_split
    )

    # Get the list of epochs trained on
    epochs = history.epoch
    # Get metrics of the model for each epoch
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

    # Use only values from the second epoch onwards because the first epoch\
    # tends to have values much larger than the rest
    for m in list_of_metrics:
        x = hist[m]
        plt.plot(epochs[1:], x[1:], label=m)

    plt.legend()
    plt.ylim([0, 1])
    plt.show()


# Load data
# ------------------------------
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()


# Pre-process data
# ------------------------------
# Normalize color values to be in the 0-1 range
x_train_normalized = x_train / 255.0
x_test_normalized = x_test / 255.0


# Set hyperparameters
# ------------------------------
learning_rate = 0.003
epochs = 50
batch_size = 4000
validation_split = 0.2

# Create the model
# ------------------------------
my_model = create_model(learning_rate)

# Train the model
# ------------------------------
epochs, hist = train_model(
    my_model, 
    x_train_normalized, 
    y_train, 
    epochs, 
    batch_size, 
    validation_split
)

# Plot the evolution of metrics over the epoch
list_of_metrics_to_plot = ['accuracy']
plot_curve(epochs, hist, list_of_metrics_to_plot)

# Evaluate the model
# ------------------------------
my_model.evaluate(
    x=x_test_normalized, 
    y=y_test, 
    batch_size=batch_size
)