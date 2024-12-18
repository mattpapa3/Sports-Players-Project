import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.neural_network import MLPClassifier

df = pd.read_csv("Hitterdata.csv")

cat_mapping = {
    "tb": 0,
    "r": 1,
    "hrb": 2
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

df = df[df['cat'] == 'tb']

df['cat'] = df['cat'].map(cat_mapping)
df['oppteam'] = df['oppteam'].map(team_mapping)
#nan_rows = df[df['avg_spin_off'].isna()]
df['avg_spin_off'] = df['avg_spin_off'].fillna(0.0)
df['avg_spin_ff'] = df['avg_spin_ff'].fillna(0.0)
df['avgvsOFF'] = df['avgvsOFF'].fillna(0.0)
df['avgvsMPHFB'] = df['avgvsMPHFB'].fillna(0.0)
df['avgvsFB'] = df['avgvsFB'].fillna(0.0)
#df.update(nan_rows)
#nan_rows = df[df['avg_spin_ff'].isna()]
#nan_rows['avg_spin_off'] = nan_rows['avg_spin_ff'].fillna(0.0)
#df.update(nan_rows)

X = df[[ "last10", "last5","log", "whip","OPSlast5", "temperature", "pitcherfip", "pitcherFBPercent", "avgvsFB","avgvsOFF","avgvsMPHFB", "avg_spin_ff", "avg_spin_off"]]
y = df["hit"]

corr_matrix = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Feature Correlation Matrix')

# Save the plot to a file
plt.savefig('totalBases_feature_correlation_matrix.png')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

print(y_train.value_counts())


parameter_space = {
    'hidden_layer_sizes': [(25,), (64,32), (64,32,16), (50,), (100,), (32,16)],
    'activation': ['tanh', 'relu', 'logistic', 'identity'],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.0001, 0.05, 0.01, 0.001],
    'learning_rate': ['constant','adaptive'],
}


# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

classifier = MLPClassifier(hidden_layer_sizes=(64, 32), alpha=0.001, activation='logistic')
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


pickle.dump(classifier, open("hittersmodel.pkl", "wb"))

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

