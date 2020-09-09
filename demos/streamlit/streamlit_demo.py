# >> streamlit run streamlit_demo.py
import streamlit as st
import pandas as pd
import numpy as np

# Global variables
# ---------------------------------------------------------------------
DATE_COLUMN = "date/time"
DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"

# Load the cached data for this function if possible
@st.cache
def load_data(num_rows):
    """Load `num_rows` rows from the data stored at `DATA_URL`.
    """
    data = pd.read_csv(DATA_URL, nrows=num_rows)
    def lowercase(x): return str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


st.title("Uber pickups in NYC")

# Load data
# ---------------------------------------------------------------------
data_load_state = st.text("...Downloading data...")
data = load_data(10000)
data_load_state.text("...Data downloaded (with cache)...")

# Preview data in a table
# ---------------------------------------------------------------------
# The table is rendered only if the checkbox is selected
if st.checkbox("Preview data"):
	st.subheader("Raw data")
	st.write(data)

# Plot an histogram for the number of pickups by hour
# ---------------------------------------------------------------------
st.subheader("Number of pickups by hour")
# Get the count of pickups for each hour in the day
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# Use the counts to plot a column chart in the page
st.bar_chart(hist_values)


# Add a map plot of pickups (filtered by hour with a slicer)
# ---------------------------------------------------------------------
st.subheader("Geographical distribution of pickups")
# Add a slider, with the 0-23 range, defaults to 17
hour_to_filter = st.slider("Filter by hour of day", 0, 23, 17)
data_filtered_by_hour = data.loc[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.map(data_filtered_by_hour)
