import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read in data using pandas
df = pd.read_csv('data.csv')

# Set theme
sns.set_style("white")

# Create scatterplot using sns
sns.scatterplot(data = df, x = "x", y = "y").set_title('Scatterplot between X and Y')

# Show plot
plt.show()
