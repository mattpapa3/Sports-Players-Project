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

df = df[df['cat'] == '3-pt']

#X = df[[ "position","opp", "last10", "oppposrank", "gamescore", "minutes", "shots", "spread"]]    # POINTS/PRA
#X = df[[ "opp", "last10", "oppposrank", "gamescore", "minutes",  "spread"]]    # Assists
#X = df[[ "last10", "oppposrank",  "gamescore", "minutes", "shots", "spread"]]    # Rebounds
X = df[[ "line",  "opp", "last5", "oppposrank", "gamescore", "shots", "spread"]]    # 3PT
y = df["hit"]

#corr_matrix = df.corr()

#plt.figure(figsize=(12, 10))
#sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
#plt.title('Feature Correlation Matrix')

# Save the plot to a file
#plt.savefig('PRANBA_feature_correlation_matrix.png')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=50)

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

#classifier = RandomForestClassifier()
#classifier = MLPClassifier(hidden_layer_sizes=(25,), activation='tanh', alpha=0.01, learning_rate='adaptive', solver='adam') #POINTS
#classifier = MLPClassifier(hidden_layer_sizes=(100,), activation='tanh', alpha=0.05, learning_rate='adaptive', solver='adam') #PRA
#classifier = MLPClassifier(hidden_layer_sizes=(25,), activation='relu', alpha=0.001, learning_rate='constant', solver='sgd') #ASSISTS
classifier = MLPClassifier(hidden_layer_sizes=(64,32,16), activation='identity', alpha=0.05, learning_rate='adaptive', solver='adam') #3PT
#classifier = MLPClassifier(hidden_layer_sizes=(32,16), activation='identity', alpha=0.0001, learning_rate='constant', solver='adam') #REBOUNDS
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
pickle.dump(classifier, open("threepointmodel.pkl", "wb"))

y_pred = classifier.predict(X_test)
#y_pred = regressor.predict(X_test)
#y_pred = best_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Feature Importance
#feature_importance = regressor.feature_importances_
#print("Feature Importance:", feature_importance)

#print('Best parameters found:\n', clf.best_params_)
#print('Best score:', clf.best_score_)

# Predict with the best model
#y_pred = clf.predict(X_test)

# Evaluate the model
#print(classification_report(y_test, y_pred))
