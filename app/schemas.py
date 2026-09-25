# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ---------- Auth Schemas ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Stock Data Schemas ----------
class StockHistoryItem(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


# ---------- Prediction Schemas ----------
class PredictionRequest(BaseModel):
    ticker: str
    model_type: str = "lstm"   # "lstm", "random_forest", "linear_regression"


class PredictionResponse(BaseModel):
    ticker: str
    model_used: str
    current_price: float
    predicted_price: float
    predicted_for_date: datetime


# ---------- Watchlist Schemas ----------
class WatchlistCreate(BaseModel):
    ticker: str


class WatchlistResponse(BaseModel):
    id: int
    ticker: str
    added_at: datetime

    class Config:
        from_attributes = True