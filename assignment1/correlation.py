import pandas as pd

## Create two pandas series

# Create x using range() function
x = pd.Series(range(20, 30))
# Create y manually
y = pd.Series([3, 1, 7, 9, 8, 14, 18, 27, 61, 32])

# Run Pearson correlation (default) on two variables
# Store in 'result' variable
result = x.corr(y)

# Print result to console
print(result)

# Store x and y in dataframe
df = pd.concat([x, y], axis=1)

# Rename columns to x and y
df.rename({0: 'x', 1: 'y'}, axis=1, inplace=True)

# Save as csv
df.to_csv("data.csv", index= False)