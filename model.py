import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
data = pd.read_csv("dataset/skills_job_roles.csv")
X = data["skills"]
y = data["job_role"]
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)
model = MultinomialNB()
model.fit(X_vec, y)
joblib.dump(model, "job_role_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model trained and saved successfully")
