# 🛡️ Agentic Fraud Detection System

An AI-powered fraud detection platform that analyzes transactions in real time using Machine Learning, FastAPI, SQLite, and Streamlit.

## 🚀 Features

- Real-time fraud prediction
- AI-generated investigation reports
- FastAPI REST API
- SQLite transaction storage
- Interactive Streamlit dashboard
- Fraud vs Legitimate analytics
- Transaction history tracking
- Risk assessment recommendations

## 🏗️ Architecture

User Input
↓
Streamlit Dashboard
↓
FastAPI Backend
↓
Machine Learning Model
↓
SQLite Database
↓
Investigation Report

## 🛠️ Tech Stack

- Python
- FastAPI
- Streamlit
- Scikit-Learn
- SQLite
- Pandas
- Plotly

## 📂 Project Structure

```bash
agentic-fraud-detection/
│
├── backend/
│   └── main.py
│
├── database/
│   ├── db.py
│   └── models.py
│
├── frontend/
│   └── app.py
│
├── models/
│   └── fraud_model.pkl
│
├── train_model.py
├── requirements.txt
└── README.md
```

## ⚡ API Endpoints

### Predict Fraud

POST /predict

### Transaction History

GET /transactions

## 📊 Dashboard

- Transaction Analysis
- Fraud Probability
- Investigation Report
- Historical Trends
- Fraud Distribution Chart

## 👨‍💻 Author

Samarth Sharma

Artificial Intelligence & Data Science Student