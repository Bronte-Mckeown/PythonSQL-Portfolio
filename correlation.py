import pandas as pd

## Create two pandas series

# Create x using range() function
x = pd.Series(range(20, 30))
# Create y manually
y = pd.Series([3, -1, 7, 9, 8, -14, 18, 27, 61, 32])

# Run Pearson correlation (default) on two variables
# Store in 'result' variable
result = x.corr(y)

# Print result to console
print(result)

# Store x and y in dataframe and save as csv
df = pd.concat([x, y], axis=1)
df.to_csv("data.csv")