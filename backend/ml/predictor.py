import numpy as np
from sklearn.ensemble import RandomForestClassifier
# Demonstration training data:
# attendance, internal, assignment, practical, quiz, previous_cgpa
X = np.array([
    [90,85,90,88,85,8.5],
    [85,80,82,85,80,8.0],
    [80,75,78,80,75,7.5],
    [75,70,72,75,70,7.0],
    [70,65,65,68,65,6.5],
    [65,60,60,62,60,6.0],
    [60,55,55,58,55,5.5],
    [50,45,48,50,45,5.0],
    [45,40,40,45,40,4.5],
    [95,92,95,94,93,9.0]
])
y = np.array([1,1,1,1,1,0,0,0,0,1])
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

def predict_risk(
    attendance, internal, assignment,
    practical, quiz, previous_cgpa
):
    features = np.array([[
        attendance, internal, assignment,
        practical, quiz, previous_cgpa
    ]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]

    return {
        "risk": "HIGH" if prediction == 0 else "LOW",
        "high_risk_probability": round(float(probability[0]) * 100, 2)
    }
