import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("pitcherstrikeoutdata.csv")

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

X = df[["opprank", "k9","kpercent",\
         "fip", "wind", "Kperwalk"]]
y = df["hit"]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

param_grid = {
    'n_estimators': [600, 700, 500],
    'max_depth': [5, 4, 3],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}


# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

classifier = RandomForestClassifier()

# Fit Model
classifier.fit(X_train, y_train)

importances = classifier.feature_importances_

# Get indices of features sorted by importance
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for i in range(X_train.shape[1]):
    print(f"{i + 1}. feature {indices[i]} ({importances[indices[i]]})")


#pickle.dump(classifier, open("strikeoutmodel.pkl", "wb"))

y_pred = classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

kf = KFold(n_splits=5, shuffle=True)

scores = cross_val_score(classifier, X, y, cv=kf, scoring='accuracy')

# Print the cross-validation scores
print(f"Cross-Validation Scores: {scores}")
print(f"Mean Cross-Validation Score: {scores.mean()}")