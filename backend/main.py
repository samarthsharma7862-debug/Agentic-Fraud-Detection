from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime

from database.db import SessionLocal, engine, Base
from database.models import TransactionLog

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agentic Fraud Detection API",
    version="2.0"
)

model = joblib.load("models/fraud_model.pkl")


class Transaction(BaseModel):
    amount: float
    transaction_hour: int
    new_device: int
    international: int


def generate_report(data):
    reasons = []

    if data.amount > 5000:
        reasons.append("High transaction amount")

    if data.transaction_hour < 6:
        reasons.append("Late-night transaction")

    if data.new_device:
        reasons.append("New device used")

    if data.international:
        reasons.append("International transaction")

    risk = "Low Risk"

    if len(reasons) >= 3:
        risk = "High Risk"
    elif len(reasons) >= 1:
        risk = "Medium Risk"

    recommendation = (
        "Block transaction and request additional verification."
        if risk == "High Risk"
        else "Monitor transaction."
    )

    return {
        "risk_level": risk,
        "reasons": reasons,
        "recommendation": recommendation
    }


@app.get("/")
def root():
    return {"message": "Agentic Fraud Detection API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(transaction: Transaction):

    df = pd.DataFrame([transaction.dict()])

    prediction = int(model.predict(df)[0])

    probability = (
        float(model.predict_proba(df)[0][1])
        if hasattr(model, "predict_proba")
        else prediction
    )

    report = generate_report(transaction)

    db = SessionLocal()

    log = TransactionLog(
        amount=transaction.amount,
        fraud_probability=probability,
        prediction=prediction,
        timestamp=str(datetime.now())
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    db.close()

    return {
        "id": log.id,
        "timestamp": log.timestamp,
        "amount": log.amount,
        "prediction": prediction,
        "fraud_probability": probability,
        "investigation_report": report
    }


@app.get("/transactions")
def get_transactions():

    db = SessionLocal()

    records = db.query(TransactionLog).all()

    result = []

    for r in records:
        result.append({
            "id": r.id,
            "amount": r.amount,
            "fraud_probability": r.fraud_probability,
            "prediction": r.prediction,
            "timestamp": r.timestamp
        })

    db.close()

    return result