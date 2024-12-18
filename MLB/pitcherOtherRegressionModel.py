import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import pickle
import seaborn as sns


df = pd.read_csv("pitcherotherdata.csv")

team_mapping = {
    "Miami Marlins" : 1,
    "New York Mets" : 2,
    "Oakland Athletics" : 3,
    "Tampa Bay Rays" : 4,
    "Cincinnati Reds" : 5,
    "Philadelphia Phillies" : 6,
    "Detroit Tigers" : 7,
    "New York Yankees" : 8,
    "Baltimore Orioles" : 9,
    "Chicago White Sox" : 10,
    "Pittsburgh Pirates" : 11,
    "Seattle Mariners" : 12,
    "Cleveland Guardians" : 13,
    "Houston Astros" : 14,
    "Minnesota Twins" : 15,
    "St. Louis Cardinals" : 16,
    "Milwaukee Brewers" : 17,   
    "Texas Rangers" : 18,
    "Chicago Cubs" : 19,
    "Washington Nationals" : 20,
    "Colorado Rockies" : 21,
    "Kansas City Royals" : 22,
    "San Francisco Giants" : 23,
    "Toronto Blue Jays" : 24,
    "Los Angeles Angels" : 25,
    "Los Angeles Dodgers" : 26,
    "Arizona Diamondbacks" : 27,
    "San Diego Padres" : 28,
    "Atlanta Braves" : 29,
    "Boston Red Sox" : 30
}

df['oppteam'] = df['oppteam'].map(team_mapping)
df = df[df['cat'] == 'era']
X = df[["line", "opprank", "last5", "inningspitchedlast3", "temperature","wind","fip"]]  # ERA
#X = df[["homeaway", "line", "opprank", "last5", "oppteam", "inningspitchedlast3", "temperature","wind", "fip"]]  # HITS ALLOWED
y = df["hit"].astype(float)

#corr_matrix = df.corr()

# Print the correlation matrix
#print(corr_matrix)

# Plot the heatmap
#plt.figure(figsize=(12, 10))
#sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
#plt.title('Feature Correlation Matrix')

# Save the plot to a file
#plt.savefig('hitsAllowed_feature_correlation_matrix.png')

# Optionally, close

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

pickle.dump(model, open("earnedRunsAllowedRegressionmodel.pkl", "wb"))