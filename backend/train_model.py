import joblib
from sklearn.linear_model import LogisticRegression
import numpy as np

# Load the preprocessed data
features = np.load('features.npy')
labels = np.load('labels.npy')
mlb = joblib.load('mlb.pkl')

# Train the logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(features, labels)

# Save the trained model
joblib.dump(model, 'trained_model.pkl')