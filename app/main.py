# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, stocks, predict, user

# Create DB tables (only if they don't exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Stock Market Prediction System",
    description="A FastAPI backend for stock trend analysis and ML-based price prediction",
    version="1.0.0",
)

# Session middleware - enables request.session (used for auth cookies)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS - allows a separate frontend (different origin) to call this API with cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(stocks.router, prefix="/api/stocks", tags=["Stocks"])
app.include_router(predict.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(user.router, prefix="/api/user", tags=["User"])


@app.get("/")
def root():
    return {"message": "Stock Market Prediction System API is running 🚀"}