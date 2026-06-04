from sqlalchemy import Column, Integer, Float, String
from database.db import Base


class TransactionLog(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float)

    fraud_probability = Column(Float)

    prediction = Column(Integer)

    timestamp = Column(String)