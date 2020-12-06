import numpy as np
import pandas as pd

start_date = np.datetime64("2016-01-01")
end_date = np.datetime64("2020-12-31")
dates = pd.date_range(start_date, end_date).date

chosen_dates = np.random.choice(dates, 10_000, replace=True)
sales_amount = np.random.randint(500, 500_000, 10_000)

df = pd.DataFrame({"Date": chosen_dates, "Sales Amount": sales_amount})
df.to_csv("sales_data.csv", index=False)