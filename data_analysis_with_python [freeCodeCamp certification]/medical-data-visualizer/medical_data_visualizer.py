import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add "overweight" column
# To determine if a person is overweight, first calculate their BMI by\
# dividing their weight in kilograms by the square of their height in\
# meters. If that value is > 25 then the person is overweight. Use the\
# value 0 for NOT overweight and the value 1 for overweight.
new_height = df["height"] / 100
bmi = df["weight"] / (new_height ** 2)
df["overweight"] = bmi.apply(
    lambda value:
        1 if value > 25
        else 0
)

# Normalize data by making 0 always good and 1 always bad
# If the value of "cholestorol" or "gluc" is 1, make the value 0; if the\
# value is more than 1, make the value 1
df["cholesterol"] = df["cholesterol"].map(
    lambda value:
        0 if value == 1
        else 1 if value > 1
        else value
)
df["gluc"] = df["gluc"].map(
    lambda value:
        0 if value == 1
        else 1 if value > 1
        else value
)


def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from "cholesterol", "gluc", "smoke", "alco", "active", and "overweight".

    # Pivot the "cardio" and "age" columns, keeping only the other columns specified.
    # "age" is kept simply to count rows in the plot
    df_cat = df.melt(
        ["cardio", "age"],
        ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )
    # Reset the index to be able to access those columns
    df_cat_index_reset = df_cat.reset_index()
    # Sort the DF by "variable" for formating preferences
    df_cat_index_reset.sort_values("variable", inplace=True)

    # Draw the count of patients for each variable, broken down by whether\
    # they have the condition. Data is plotted for both cardio=0 and\
    # for cardio=1
    fig = sns.catplot(
        data=df_cat_index_reset,
        x="variable",
        col="cardio",
        hue="value",
        kind="count"
    )
    # Change the Y-axis range from 0 to an automatic upper limit
    plt.ylim(0, None)
    plt.ylabel("total")

    fig.savefig("catplot.png")


def draw_heat_map():
    # Clean the data
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = round(df_heat.corr(), 1)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw the heatmap with "sns.heatmap()"
    ax = sns.heatmap(
        corr,
        mask=mask,
        square=True,
        annot=True,
    )

    fig.savefig("heatmap.png")


draw_cat_plot()
draw_heat_map()
