import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to "date".)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df.set_index(["date"], inplace=True)

# Clean data
df = df[
    (df["value"] > df["value"].quantile(0.025)) &
    (df["value"] < df["value"].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots()
    ax.plot(df.index, df["value"], color="red")

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    fig.set_size_inches(15, 4.5)

    # Save image
    fig.savefig("line_plot.png")


def draw_bar_plot():
    # https://stackoverflow.com/questions/47796264/function-to-create-grouped-bar-plot
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August", "September",
        "October", "November", "December"
    ]

    df_bar = df.copy()

    # Create a column for the month recorded
    df_bar["Month"] = df.index.month
    # Replace month numbers by their name
    df_bar["Month"] = df_bar["Month"].apply(
        lambda m: months[m-1]
    )
    # Make this a categorical column so it can be sorted by the order of values in the `months` list
    df_bar["Month"] = pd.Categorical(
        df_bar["Month"],
        categories=months
    )

    # Create a column for the year recorded
    df_bar["Year"] = df.index.year

    # Pivot the years against the months, using the average page views as the values
    df_bar = pd.pivot_table(
        df_bar,
        values="value",
        index="Year",
        columns="Month",
        aggfunc=np.mean
    )

    # Draw bar plot
    ax = df_bar.plot(kind="bar")
    fig = ax.get_figure()
    fig.set_size_inches(7, 6)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    # Save image
    fig.savefig("bar_plot.png")


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    # Create a column for the year recorded
    df_box["year"] = [d.year for d in df_box.index]
    months = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]
    # Create a column for the month recorded
    df_box["month"] = [d.strftime("%b") for d in df_box.index]
    # Make it Categorical to sort by the proper month order (order of\
    # the `months` list elements)
    df_box["month"] = pd.Categorical(df_box["month"], categories=months)

    # Create a two subplots in a 1 row by 2 columns shape
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

    # Draw boxplots for each situation
    sns.boxplot(data=df_box, x="year", y="value", ax=ax[0])
    sns.boxplot(data=df_box, x="month", y="value", ax=ax[1])

    # Change the title and labels for each subplot
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image
    fig.savefig("box_plot.png")


draw_line_plot()
draw_bar_plot()
draw_box_plot()
