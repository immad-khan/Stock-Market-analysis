# app/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    watchlist = relationship("Watchlist", back_populates="owner")
    predictions = relationship("PredictionHistory", back_populates="owner")


class Watchlist(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="watchlist")


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    model_used = Column(String, nullable=False)       # "LSTM", "RandomForest", "LinearRegression"
    predicted_price = Column(Float, nullable=False)
    actual_price_at_prediction = Column(Float, nullable=True)
    predicted_for_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="predictions")