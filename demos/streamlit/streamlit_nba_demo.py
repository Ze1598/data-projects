import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
st.set_option("deprecation.showfileUploaderEncoding", False)
import os

st.title("NBA Player Stats Explorer")
st.markdown(
    "Data source: [basketball-reference.com](https://www.basketball-reference.com)")


@st.cache
def load_data(year: int) -> pd.DataFrame:
    """Scrape a table of data from the web and pre-process it.
    """
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    # `read_html` returns a list of DataFrames but we are interested in the first one
    scraped_tables = pd.read_html(url, header=0)
    data = scraped_tables[0]
    # Delete rows where the "Age" column has a value of "Age", using their index
    data.drop(data[data["Age"] == "Age"].index, inplace=True)
    data.fillna(0, inplace=True)
    # The "Rk" is not needed because the DataFrame has its own index
    data.drop(["Rk"], axis="columns", inplace=True)
    return data


# Sidebar - Title and year selection
# -----------------------------------------------
st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox(
    "Year",
    list(reversed(range(1950, 2020)))
)

data = load_data(selected_year)


# Sidebar - Team selection
# -----------------------------------------------
sorted_teams = sorted(data["Tm"].unique())
# Returns an array of teams selected
selected_teams = st.sidebar.multiselect("Team", sorted_teams, sorted_teams)

# Sidebar - Position selection
# -----------------------------------------------
player_positions = ["C", "PF", "SF", "PG", "SG"]
selected_pos = st.sidebar.multiselect(
    "Position", player_positions, player_positions)

# Filter and display data based on the filters chosen
# -----------------------------------------------
data_filtered = data[(data["Tm"].isin(selected_teams)) &
                     (data["Pos"].isin(selected_pos))]
st.header("Player Stats of Selected Team(s)")
st.write(
    f"The current selection includes {data_filtered.shape[0]} rows and {data_filtered.shape[1]} columns.")
st.dataframe(data_filtered)

# Create a CSV and a download link for it
# -----------------------------------------------
csv_file = data_filtered.to_csv(index=False)
# Convert the CSV to a base 64 bytes object
encoded_csv = base64.b64encode(csv_file.encode()).decode()
href = f'<a href="data:file/csv;base64,{encoded_csv}" download="playerstats.csv">Download as CSV</a>'
st.markdown(href, unsafe_allow_html=True)


# Create a heatmap for the data
# -----------------------------------------------
if st.button("Heatmap"):
    st.header("Intercorrelation Matrix Heatmap")

    # Save the data to a CSV and load it to update column data types
    data_filtered.to_csv("__output.csv", index=False)
    df = pd.read_csv("__output.csv")
    os.remove("__output.csv")

    # Since the heatmap is symmetric across the left diagonal, hide the top half
    # Create a correlation matrix
    corr = df.corr()
    # Create an array of zeroes using the same shape as the correlation matrix
    mask = np.zeros_like(corr)
    # Set to True the values above the diagonal, that is, the values to mask or hide
    mask[np.triu_indices_from(mask)] = True

    # Draw the heatmatp
    with sns.axes_style("white"):
    	fig, ax = plt.subplots(figsize=(7, 5))
    	ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    # Display the plot
    st.pyplot()
