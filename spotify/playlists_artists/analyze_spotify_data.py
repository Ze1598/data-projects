import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pre_process_data(file_name: str) -> pd.DataFrame:
    """
    Load the data from a CSV file and sort it data by the "Frequency"
    column, in descending order.
    """
    # Load the CSV with the artist frequency data. The first column has the indices
    dataset = pd.read_csv(file_name)

    # Sort the dataset by "Frequency", in descending order, and reset the indices
    dataset = dataset.sort_values(
        "Frequency",
        ascending=False
    ).reset_index(drop=True)

    return dataset


def plot_column_chart(data: pd.DataFrame) -> None:
    # Plot a column chart with Plotly (Artists vs Frequency)
    fig = px.bar(
        data.head(n=10), x="Artist", y="Frequency",
        text="Frequency",
        title=f"Top 10 Artists (out of {data.shape[0]} artists)"
    )

    # Add the data labels inside the columns
    fig.update_traces(
        textposition="inside"
    )

    # Adjust the font and center the title
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        uniformtext_minsize=14,
        uniformtext_mode="hide",
        title_x=0.5
    )

    # Display the finalized plot
    fig.show()


if __name__ == "__main__":
    # CSV with the data
    file_name = "artists_frequencies.csv"
    # Load the data
    dataset = pre_process_data(file_name)
    # Plot the data in a column chart
    plot_column_chart(dataset)
