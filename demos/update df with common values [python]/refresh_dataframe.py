import pandas as pd
import numpy as np
"""
Assuming new DF are generated over time for a group of people, update
the previous DF with the new rows of data. 

For people who appear in both the DFs, only the data from the new DF
is kept, assuming this "latest" data has all their information up-to-date. 

New people in the new DF are simply appended to the old DF. 

However, people who only appear in the first DF are considered to not 
belong to the group anymore, so their data is changed to default values. 
The only thing that remains unchanged is their id, to signify that someone
with that id has already existed in the group.
"""

# Original DF with 4 people
original = pd.DataFrame({
	"id": [1, 2, 3, 4], 
	"name": ["Michael", "Jim", "Pam", "Dwight"], 
	"age":[22, 31, 12, 59]}
)
# Make a copy so we don't modify the original DF directly
original_copy = original.copy(deep=True)
# A new DF generated at a later time. It has two new people (ids 5 and 6)\
# and is missing one person from the previous data (id 2)
new_data = pd.DataFrame({
	"id": [1, 3, 4, 5, 6], 
	"name": ["Michael", "Pam", "Dwight", "Kevin", "Stanley"], 
	"age":[22, 12, 59, 120, 74]
})

# Set the name and age of missing people to default values
original_copy.loc[~original_copy["id"].isin(new_data["id"]), "name"] = ""
original_copy.loc[~original_copy["id"].isin(new_data["id"]), "age"] = -1

# Append the new DF to the modified original data to create a single DF
updated = original_copy.append(new_data, ignore_index=True)
# Since some people were in both DFs, remove rows with duplicates ids,\
# that is, based on the id, keep only the last instance of that id (assume\
# the last occurrence is the one with their information up to date)
updated = updated.drop_duplicates(["id"], keep="last")
# Sort the data by id after duplicate removal
updated.sort_values("id", inplace=True)
# Reset the DF index after all the transformations (dropping the previous index)
updated.reset_index(drop=True, inplace=True)

print("---Original group:\n", original)
print("---Updated group:\n", updated)
