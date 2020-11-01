import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Read data from file
data = pd.read_csv("epa-sea-level.csv")

# Create scatter plot
# -------------------
plt.scatter(
    data["Year"], 
    data["CSIRO Adjusted Sea Level"], 
    label="Recorded sea levels"
)

# Create first line of best fit
# -----------------------------
linear_regression = linregress(data["Year"], data["CSIRO Adjusted Sea Level"])
slope = linear_regression[0]
intercept = linear_regression[1]

# Create a Series with the years until 2050
first_year = min(data["Year"])
reg_years = pd.Series(list(range(first_year, 2051)))

# Calculate the Y-values for the regression line
regression_line = intercept + slope * reg_years
# Plot the regression line
plt.plot(reg_years, regression_line, "red", label="Predicted sea levels")

# Create second line of best fit
# ------------------------------
# Create a Series with the years specified
reg_years_v2 = pd.Series(list(range(2000, 2051)))

# Calculate a new regression line, for a subset of the data
filtered_data = data.query("Year >= 2000")
regression_line_v2 = linregress(filtered_data["Year"], filtered_data["CSIRO Adjusted Sea Level"])
slope_v2 = regression_line_v2[0]
intercept_v2 = regression_line_v2[1]

# Calculate the Y-values for the regression line
regression_line_v2 = intercept_v2 + slope_v2 * reg_years_v2
plt.plot(reg_years_v2, regression_line_v2, "orange", label="Predicted sea levels (v2)")

# Format plot
# --------------------
plt.title("Rise in Sea Level")
plt.xlabel("Year")
plt.ylabel("Sea Level (inches)")
plt.legend()

# Save plot
# --------------------
plt.savefig("sea_level_plot.png")