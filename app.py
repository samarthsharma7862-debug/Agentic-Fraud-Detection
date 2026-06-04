import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model
model = joblib.load("fraud_model.pkl")

st.set_page_config(
    page_title="Agentic Fraud Detection",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Real-Time Fraud Detection System")

st.write("Predict fraudulent transactions using Machine Learning")

# Sidebar Inputs
st.sidebar.header("Transaction Details")

amount = st.sidebar.number_input(
    "Transaction Amount",
    min_value=0.0,
    value=5000.0
)

transaction_hour = st.sidebar.slider(
    "Transaction Hour",
    0,
    23,
    12
)

new_device = st.sidebar.selectbox(
    "New Device?",
    [0, 1]
)

international = st.sidebar.selectbox(
    "International Transaction?",
    [0, 1]
)

# Prediction
input_data = pd.DataFrame({
    "amount": [amount],
    "transaction_hour": [transaction_hour],
    "new_device": [new_device],
    "international": [international]
})

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

# Display Results
st.subheader("Prediction Result")

if prediction == 1:
    st.error("🚨 FRAUD DETECTED")
else:
    st.success("✅ Legitimate Transaction")

st.metric(
    label="Fraud Probability",
    value=f"{probability:.2%}"
)

st.subheader("Transaction Summary")
st.dataframe(input_data)

# Explanation Engine
st.subheader("AI Investigation Report")

reasons = []

if amount > 7000:
    reasons.append("High transaction amount")

if transaction_hour < 5:
    reasons.append("Late-night transaction")

if new_device:
    reasons.append("New device detected")

if international:
    reasons.append("International transaction")

if len(reasons) == 0:
    st.success("No suspicious patterns detected.")
else:
    for reason in reasons:
        st.write("•", reason)