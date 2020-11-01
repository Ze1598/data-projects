import pandas as pd

# Read data from file
df = pd.read_csv("adult.data.csv")
num_rows = df.shape[0]

# How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
race_count = df[["race", "age"]]\
    .groupby(["race"])\
    .count()\
    .sort_values("age", ascending=False)["age"]

# What is the average age of men?
average_age_men = df.query("sex == 'Male'")["age"]\
    .mean()
average_age_men = round(average_age_men, 1)

# What is the percentage of people who have a Bachelor's degree?
num_bachelors = df\
    .query("education == 'Bachelors'")\
    .shape[0]
percentage_bachelors = round(num_bachelors / num_rows * 100, 1)

# What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
# What percentage of people without advanced education make more than 50K?

# with and without `Bachelors`, `Masters`, or `Doctorate`
higher_ed_df = df.query(
    "education == 'Bachelors' or education == 'Masters' or education == 'Doctorate'")
more_than_50k_higher = higher_ed_df.query("salary == '>50K'").shape[0]

lower_ed_df = df.query(
    "education != 'Bachelors' and education != 'Masters' and education != 'Doctorate'")
more_than_50k_lower = lower_ed_df.query("salary == '>50K'").shape[0]

# percentage with salary >50K
higher_education_rich = round(
    more_than_50k_higher / higher_ed_df.shape[0] * 100, 1)
lower_education_rich = round(
    more_than_50k_lower / lower_ed_df.shape[0] * 100, 1)

# What is the minimum number of hours a person works per week (hours-per-week feature)?
min_work_hours = df["hours-per-week"].min()

# What percentage of the people who work the minimum number of hours per week have a salary of >50K?
min_workers = df[df["hours-per-week"] == min_work_hours]
num_min_workers = min_workers.shape[0]
num_min_workers_rich = min_workers.query("salary == '>50K'").shape[0]

rich_percentage = round(num_min_workers_rich / num_min_workers * 100, 1)

# What country has the highest percentage of people that earn >50K?
num_rich_by_country = df[["salary", "native-country"]]\
    .query("salary == '>50K'")\
    .groupby("native-country")\
    .count()
num_by_country = df[["salary", "native-country"]]\
    .groupby("native-country")\
    .count()
rich_percent_by_country = round(num_rich_by_country / num_by_country * 100, 1)\
    .sort_values("salary", ascending=False)

highest_earning_country_percentage = rich_percent_by_country.iloc[0]["salary"]

highest_earning_country = rich_percent_by_country.iloc[0].name

# Identify the most popular occupation for those who earn >50K in India.
indian_rich = df[(df["native-country"] == "India") & (df["salary"] == ">50K")]
indian_top_occupations = indian_rich[["age", "occupation"]]\
    .groupby("occupation")\
    .count()\
    .sort_values("age", ascending=False)
top_IN_occupation = indian_top_occupations.iloc[0].name

print(f"Number of each race:\n{race_count}")
print(f"Average age of men: {average_age_men}")
print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
print(f"Min work time: {min_work_hours} hours/week")
print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
print(f"Country with highest percentage of rich: {highest_earning_country}")
print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
print(f"Top occupations in India: {top_IN_occupation}")
