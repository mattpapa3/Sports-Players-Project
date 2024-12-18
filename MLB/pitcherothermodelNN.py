import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

df = pd.read_csv("pitcherotherdata.csv")

cat_mapping = {
    "era": 0,
    "hits": 1,
    "outs": 2
}

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

df = df[df['cat'] == 'era']
#df['cat'] = df['cat'].map(cat_mapping)
df['oppteam'] = df['oppteam'].map(team_mapping)

# Earned Runs
X = df[["line", "opprank", "last5", "inningspitchedlast3", "temperature","wind","fip"]]

 #Hits Allowed
#X = df[[ "homeaway", "line",  "inningspitchedlast3",\
 #         "temperature", "fip"]]

#Pitching Outs
#X = df[[ "homeaway","inningspitchedlast3",\
 #         "temperature", "fip", "overunder"]]
y = df["hit"]

#corr_matrix = df.corr()

# Print the correlation matrix
#print(corr_matrix)

# Plot the heatmap
#plt.figure(figsize=(12, 10))
#sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
#plt.title('Feature Correlation Matrix')

# Save the plot to a file
#plt.savefig('hitsAllowed_feature_correlation_matrix.png')

# Optionally, close the plot to free up memory
#plt.close()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

parameter_space = {
    'hidden_layer_sizes': [(25,), (64,32), (64,32,16), (50,), (100,)],
    'activation': ['tanh', 'relu', 'logistic', 'identity'],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.0001, 0.01, 0.001],
    'learning_rate': ['constant'],
}


# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Earned Runs Classifier
#classifier = MLPClassifier(hidden_layer_sizes=(64,32,16), alpha=0.001, activation='identity')

classifier = MLPClassifier(hidden_layer_sizes=(64,32), activation='relu', solver='sgd', alpha=0.001, learning_rate='adaptive')
#classifier = MLPClassifier(hidden_layer_sizes=(25,), activation='tanh', alpha=0.01)
#clf = GridSearchCV(classifier, parameter_space, n_jobs=-1, cv=5)

# Fit Model
classifier.fit(X_train, y_train)

#importances = classifier.feature_importances_

# Get indices of features sorted by importance
#indices = np.argsort(importances)[::-1]

# Print the feature ranking
#print("Feature ranking:")

#for i in range(X_train.shape[1]):
#    print(f"{i + 1}. feature {indices[i]} ({importances[indices[i]]})")


pickle.dump(classifier, open("earnedRunsmodel.pkl", "wb"))

y_pred = classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

kf = KFold(n_splits=5, shuffle=True)
scores = cross_val_score(classifier, X, y, cv=kf, scoring='accuracy')

# Print the cross-validation scores
print(f"Cross-Validation Scores: {scores}")
print(f"Mean Cross-Validation Score: {scores.mean()}")

#print('Best parameters found:\n', clf.best_params_)
#print('Best score:', clf.best_score_)

# Predict with the best model
#y_pred = clf.predict(X_test)

# Evaluate the model
#print(classification_report(y_test, y_pred))