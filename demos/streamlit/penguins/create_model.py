import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

penguins = pd.read_csv("data\\penguins.csv")

# Pre-process data
# ------------------------------
# One-hot encode the following columns (removing the original columns)
cols_to_encode = ["sex", "island"]
for column in cols_to_encode:
    one_hot_encoded = pd.get_dummies(penguins[column], prefix=column)
    penguins = pd.concat([penguins, one_hot_encoded], axis="columns")
    penguins.drop([column], axis="columns", inplace=True)

# Map the label classes to numeric values
class_map = {"Adelie": 0, "Chinstrap": 1, "Gentoo": 2}
penguins["species"] = penguins["species"].apply(lambda x: class_map[x])

# Separate features and labels
# ------------------------------
features = penguins.drop("species", axis="columns")
labels = penguins["species"]

# Create and train the model
# ------------------------------
model = RandomForestClassifier()
model.fit(features, labels)

# Export the trained model to a pickle file
# ------------------------------
with open("penguins_model.pkl", "wb") as f:
	pickle.dump(model, f)