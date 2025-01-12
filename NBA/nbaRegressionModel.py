import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from sklearn.preprocessing import StandardScaler


df = pd.read_csv("/root/propscode/propscode/NBAdata.csv")

position_mapping = {
    "Guard": 0,
    "Point Guard": 1,
    "Shooting Guard": 2,
    "Small Forward": 3,
    "Power Forward": 4,
    "Center": 5,
    "Forward": 6
}

cat_mapping = {
    "3-pt": 0,
    "points": 1,
    "assists": 2,
    "pra": 3,
    "rebounds": 4
}

team_mapping = {
    "Boston" : 1,
    "Brooklyn" : 2,
    "New York" : 3,
    "Philadelphia" : 4,
    "Toronto" : 5,
    "Golden State" : 6,
    "LA Clippers" : 7,
    "LA Lakers" : 8,
    "Phoenix" : 9,
    "Sacramento" : 10,
    "Chicago" : 11,
    "Cleveland" : 12,
    "Detroit" : 13,
    "Indiana" : 14,
    "Milwaukee" : 15,
    "Atlanta" : 16,
    "Charlotte" : 17,   
    "Miami" : 18,
    "Orlando" : 19,
    "Washington" : 20,
    "Denver" : 21,
    "Minnesota" : 22,
    "Okla City" : 23,
    "Portland" : 24,
    "Utah" : 25,
    "Dallas" : 26,
    "Houston" : 27,
    "Memphis" : 28,
    "New Orleans" : 29,
    "San Antonio" : 30
}

df['position'] = df['position'].map(position_mapping)
#df['cat'] = df['cat'].map(cat_mapping)
df['oppteam'] = df['oppteam'].map(team_mapping)
#df.fillna(df.mean(), inplace=True)
df = df[df['cat'] == 'points']

X = df[[ "line","opp", "last10", "oppposrank", "gamescore", "minutes", "shots", "spread"]]    # POINTS
#X = df[[ "line","position","opp", "last10", "oppposrank", "gamescore", "minutes", "shots", "spread"]] #PRA
#X = df[[ "homeaway", "line","position","opp", "last10", "last5", "oppposrank", "gamescore", "minutes", "spread"]]    # Assists
#X = df[[ "line","position","last10", "last5", "oppposrank", "gamescore", "minutes", "shots", "spread"]]    # Rebounds
#X = df[[ "line",  "opp", "last10", "last5","oppposrank", "gamescore", "minutes", "shots", "spread"]]    # 3PT
#X = df[["line", "position", "opp", "last10", "oppposrank", "minutes", "shots"]]  # Steals
#X = df[["homeaway", "line", "opp", "last10", "last5","oppteam", "gamescore", "minutes", "shots", "spread"]]  # Blocks
y = df["hit"].astype(float)

# corr_matrix = df.corr()
# plt.figure(figsize=(12, 10))
# sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
# plt.title('Feature Correlation Matrix')

# #Save the plot to a file
# plt.savefig('3PT_feature_correlation_matrix.png')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# sc = StandardScaler()
# scaler = sc.fit(X_train)
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)
# Create and train the model
model = GradientBoostingRegressor()
model.fit(X_train.values, y_train.values)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

#pickle.dump(model, open("reboundsRegressionmodel.pkl", "wb"))
