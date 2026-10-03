import pickle
import numpy as np

with open('ml/saved_models/model.pkl', 'rb') as f:
    model = pickle.load(f)
    print("Model loaded from model.pkl")

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
