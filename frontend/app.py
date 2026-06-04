import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Agentic Fraud Detection System",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Real-Time Agentic Fraud Detection System")
st.write("End-to-end AI fraud detection with FastAPI, ML model, SQLite, and investigation reports.")

st.sidebar.header("Transaction Input")

amount = st.sidebar.number_input("Transaction Amount", min_value=0.0, value=9000.0)
transaction_hour = st.sidebar.slider("Transaction Hour", 0, 23, 2)
new_device = st.sidebar.selectbox("New Device Used?", [0, 1])
international = st.sidebar.selectbox("International Transaction?", [0, 1])

if st.sidebar.button("Analyze Transaction"):
    payload = {
        "amount": amount,
        "transaction_hour": transaction_hour,
        "new_device": new_device,
        "international": international
    }

    response = requests.post(f"{API_URL}/predict", json=payload)

    if response.status_code == 200:
        result = response.json()

        st.subheader("Prediction Result")

        if result["prediction"] == 1:
            st.error("🚨 Fraud Detected")
        else:
            st.success("✅ Legitimate Transaction")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transaction ID", result["id"])
        col2.metric("Fraud Probability", f"{result['fraud_probability'] * 100:.2f}%")
        col3.metric("Amount", f"₹{result['amount']}")

        st.subheader("AI Investigation Report")

        report = result["investigation_report"]

        st.write("**Risk Level:**", report["risk_level"])

        st.write("**Reasons:**")
        if report["reasons"]:
            for reason in report["reasons"]:
                st.write(f"- {reason}")
        else:
            st.write("- No suspicious pattern found")

        st.write("**Recommendation:**", report["recommendation"])

    else:
        st.error("API request failed. Make sure FastAPI server is running.")


st.markdown("---")
st.subheader("Stored Transaction History")

try:
    history_response = requests.get(f"{API_URL}/transactions")

    if history_response.status_code == 200:
        data = history_response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)

            st.dataframe(df, use_container_width=True)

            total_transactions = len(df)
            fraud_count = int(df["prediction"].sum())
            legit_count = total_transactions - fraud_count

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Transactions", total_transactions)
            col2.metric("Fraud Transactions", fraud_count)
            col3.metric("Legitimate Transactions", legit_count)

            fig = px.pie(
                names=["Legitimate", "Fraud"],
                values=[legit_count, fraud_count],
                title="Fraud vs Legitimate Transactions"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No transactions stored yet.")

    else:
        st.warning("Could not fetch transaction history.")

except Exception:
    st.error("FastAPI backend is not running. Start it using: uvicorn backend.main:app --reload")