'''

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB

#Training Multinomial Naive Bayes Model to filter Youtube Spam comments

f = pd.read_csv('Youtube02-KatyPerry.csv')
X = df["CONTENT"]
y = df["CLASS"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

#Sklearn Training Pipeline
text_clf = Pipeline([
    ('tfidf', TfidfVectorizer()), #needed to convert text to machine usable/numeric data
    ('clf', MultinomialNB())
])

#hyperparameters
param_grid = {
    'tfidf__max_features': [500, 1000, 5000],
    'tfidf__ngram_range': [(1, 1), (1, 2)], 
    'clf__alpha': [0.1, 0.01, 0.001]
}

#hyperparameter tuning
grid_search = GridSearchCV(text_clf, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)
print(grid_search.predict(["I love your videos"]))

print("Accuracy: " + str(grid_search.score(X_test, y_test)))


best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

#save model
with open('spam_model.pkl', 'wb') as model_file:
    pickle.dump(best_model, model_file)

#[0]
#Accuracy: 0.9428571428571428

#test youtube spam model(Accuracy: 94.28%)

with open('spam_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Make predictions using the loaded model
y_pred = loaded_model.predict(["Go here to see my X rated content", "Python is a good programming language", "Hello"])

print("Predicted Label:", y_pred)

#Predicted Label: [1 0 0]

'''
