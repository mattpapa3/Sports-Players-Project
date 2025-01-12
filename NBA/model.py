import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

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

df['position'] = df['position'].map(position_mapping)
#df['cat'] = df['cat'].map(cat_mapping)
df['oppteam'] = df['oppteam'].map(team_mapping)

df = df[df['cat'] == 'rebounds']
#df = df.sample(frac = 1)
# nan_rows = df.isna().any(axis=1).sum()

# print("Number of samples with NaN values:", nan_rows)
#df.dropna(inplace=True)

# X = df[[ "line","opp", "last10", "oppposrank", "gamescore", "minutes", "shots", "spread"]]    # POINTS
# X=df[[ "line","position","opp", "last10", "oppposrank", "gamescore", "minutes", "shots", "spread"]] #PRA
# X = df[[ "homeaway", "line", "opp", "last10", "last5", "oppposrank", "gamescore", "minutes", "spread"]]    # Assists
X = df[[ "line","last10", "last5","oppposrank", "gamescore", "minutes", "shots", "spread"]]    # Rebounds
# X = df[[ "line",  "opp", "last10", "last5","oppposrank", "gamescore", "minutes", "shots", "spread"]]    # 3PT
# X = df[["line", "position", "opp", "last10", "last5", "oppposrank", "minutes", "shots"]]  # Steals
#X = df[["homeaway", "line", "position","opp", "last10", "last5", "gamescore", "minutes", "shots", "spread"]]  # Blocks
y = df["hit"]

# corr_matrix = df.corr()

# plt.figure(figsize=(12, 10))
# sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
# plt.title('Feature Correlation Matrix')

# #Save the plot to a file
# plt.savefig('Rebounds_feature_correlation_matrix.png')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

parameter_space = {
    'hidden_layer_sizes': [(25,), (64,32), (64,32,16), (50,), (100,), (32,16)],
    'activation': ['tanh', 'relu', 'logistic', 'identity'],
    'solver': ['sgd', 'adam', 'lbfgs'],
    'alpha': [0.0001, 0.05, 0.01, 0.001],
    'learning_rate': ['constant','adaptive'],
}


# Feature Scaling
# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)
#classifier = RandomForestClassifier()
# classifier = MLPClassifier(hidden_layer_sizes=(64,32,16), activation='logistic', alpha=0.001, learning_rate='adaptive', solver='adam', verbose=False, learning_rate_init=0.0005, max_iter=1000) #POINTS
# classifier = MLPClassifier(hidden_layer_sizes=(100,), activation='logistic', alpha=0.0005, learning_rate='adaptive', solver='adam', verbose=False) #PRA
# classifier = MLPClassifier(hidden_layer_sizes=(64,32), activation='logistic', alpha=0.01, learning_rate='adaptive', solver='adam', verbose=True) #PRA2
# classifier = MLPClassifier(hidden_layer_sizes=(32,16), activation='relu', alpha=0.001, learning_rate='adaptive', solver='adam', verbose=True, max_iter=500) #ASSISTS
# classifier = MLPClassifier(hidden_layer_sizes=(64,32), activation='logistic', alpha=0.001, learning_rate='adaptive', solver='adam', verbose=False) #3PT
classifier = MLPClassifier(hidden_layer_sizes=(32,16), activation='logistic', alpha=0.0001, learning_rate='adaptive', solver='adam', learning_rate_init=0.0005, verbose=False) #REBOUNDS
# classifier = MLPClassifier(hidden_layer_sizes=(64, 32, 16), activation='logistic', alpha=0.005, learning_rate='adaptive', solver='adam') #Steals
# classifier = MLPClassifier(hidden_layer_sizes=(64, 32, 16), activation='logistic', alpha=0.001, learning_rate='adaptive', solver='adam') #BLOCKS
#grid_search = GridSearchCV(estimator=classifier, param_grid=param_grid, 
 #                          scoring='neg_mean_squared_error', cv=5, verbose=2, n_jobs=-1)

#clf = GridSearchCV(classifier, parameter_space, n_jobs=-1, cv=5)

# Fit Model
classifier.fit(X_train, y_train)

#grid_search.fit(X_train, y_train)

# Get the best parameters and best model from GridSearchCV
#best_params = grid_search.best_params_
#print("Best Parameters:", best_params)
#best_model = grid_search.best_estimator_
pickle.dump(classifier, open("reboundsmodel.pkl", "wb"))

y_pred = classifier.predict(X_test)
train_acc = classifier.score(X_train, y_train)
#y_pred = regressor.predict(X_test)
#y_pred = best_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(f"Training Accuracy: {train_acc:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
scores = cross_val_score(classifier, X_train, y_train, cv=5)
print("Cross-Validation Scores:", np.mean(scores))
print(scores)
#print('Best parameters found:\n', clf.best_params_)
#print('Best score:', clf.best_score_)

# Predict with the best model
#y_pred = clf.predict(X_test)

# Evaluate the model
#print(classification_report(y_test, y_pred))
