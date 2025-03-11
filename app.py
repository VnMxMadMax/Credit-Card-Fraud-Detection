import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("D://Projects and hackathons//Credit Card Fraud Detection//fraud_detection_model.pkl")

# Streamlit Web App
st.title("💳 Credit Card Fraud Detection")

st.write("Enter transaction details below:")

# User inputs (create 29 feature inputs)
features = []
for i in range(29):
    value = st.number_input(f"Feature {i+1}", value=0.0)
    features.append(value)

# Convert input to NumPy array
features = np.array(features).reshape(1, -1)

# Predict button
if st.button("Check for Fraud"):
    prediction = model.predict(features)[0]
    if prediction == 1:
        st.error("🚨 Fraudulent Transaction Detected!")
    else:
        st.success("✅ Transaction is Safe.")