# app/ml/data_fetch.py

import yfinance as yf
import pandas as pd
from app.ml.constants import TRAINING_PERIOD, INTERVAL


def fetch_stock_data(ticker: str, period: str = TRAINING_PERIOD, interval: str = INTERVAL) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker using yfinance.
    
    Returns DataFrame with: Date, Open, High, Low, Close, Volume
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period, interval=interval)

    if df.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Please check the symbol.")

    df = df.reset_index()

    # Keep only required columns
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

    return df


def fetch_latest_data(ticker: str, days: int = 90) -> pd.DataFrame:
    """
    Fetch latest market data for real-time prediction.
    Used at inference time (when user clicks Predict).
    """
    df = fetch_stock_data(ticker, period=f"{days}d", interval="1d")
    return df


if __name__ == "__main__":
    from app.ml.constants import TICKERS

    print("Fetching sample data for all tickers...\n")
    for symbol in TICKERS:
        try:
            data = fetch_stock_data(symbol, period="1mo")
            print(f"✅ {symbol}: {len(data)} rows | Latest Close: {data['Close'].iloc[-1]:.2f}")
        except Exception as e:
            print(f"❌ {symbol}: {e}")