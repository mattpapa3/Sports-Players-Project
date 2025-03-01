import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression


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
    "rebounds": 4,
    "blocks": 5,
    "steals": 6
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

def american_odds_to_percentage(odds):
    """Converts American odds to percentage."""
    if int(odds) > 0:
        return round(100 / (int(odds) + 100), 4)
    return round(-int(odds) / (-int(odds) + 100),4)

df = pd.read_csv("/root/propscode/propscode/NBA/oddsdata.csv")
df['odds'] = df['odds'].str.replace('−', '-', regex=False).astype(int)
df['underodds'] = df['underodds'].str.replace('−', '-', regex=False).astype(int)
df['position'] = df['position'].map(position_mapping)
df['cat'] = df['cat'].map(cat_mapping)
df['oppteam'] = df['oppteam'].map(team_mapping)
df['spread'] = df['spread'].str.split('-', 1).str[1]
df['spread'] = df['spread'].astype(float)
# df['odds'] = df['odds'].apply(american_odds_to_percentage)
# df['underodds'] = df['underodds'].apply(american_odds_to_percentage)

# correlation_with_overOdds = df.corr()['line']
# print(correlation_with_overOdds)

# print("\n\n")

# correlation_with_overOdds = df.corr()['underodds']
# print(correlation_with_overOdds)


X = df.drop(columns=['underodds', 'hit', 'minutes', 'oppteam', 'injuredStarters', 'injuredBench', 'id', 'odds', 'date',\
    'shootingPLast3', 'shootingPLast5', 'favorite', 'gamescore'])
y = df['odds']
# y = df["underodds"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# sc = StandardScaler()
# scaler = sc.fit(X_train)
# X_train = scaler.transform(X_train)
# X_test = scaler.transform(X_test)
#{'activation': 'logistic', 'alpha': 0.01, 'hidden_layer_sizes': (100,), 'learning_rate_init': 0.001, 'solver': 'adam'}
model = GradientBoostingRegressor()
model.fit(X_train.values, y_train.values)

# Make predictions
y_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

# Evaluate the model
r2 = r2_score(y_test, y_pred)
train_mse = mean_squared_error(y_train, y_train_pred)
test_mse = mean_squared_error(y_test, y_pred)

print(f"Training MSE: {train_mse}")
print(f"Testing MSE: {test_mse}")
print(f'R-squared: {r2}')
pickle.dump(model, open("overOddsmodel.pkl", "wb"))
# pickle.dump(model, open("linesModel.pkl", "wb"))