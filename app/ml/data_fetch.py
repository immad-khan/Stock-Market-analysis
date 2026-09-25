import pandas as pd
import yfinance as yf

from app.ml.constants import TRAINING_PERIOD, LOOKBACK_DAYS


def fetch_stock_data(symbol: str, period: str = TRAINING_PERIOD) -> pd.DataFrame:
    """Fetch and clean daily historical OHLCV data."""
    df = yf.Ticker(symbol).history(
        period=period,
        interval="1d",
        auto_adjust=True,
        actions=False,
    )

    if df.empty:
        raise ValueError(
            f"No data returned for {symbol}. Check the symbol, connection, "
            "or Yahoo Finance availability."
        )

    df = df.reset_index()
    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = df[columns].copy()

    # Keep the exchange's calendar date without the timezone.
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    for column in columns[1:]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = (
        df.dropna(subset=columns)
        .drop_duplicates(subset="Date", keep="last")
        .sort_values("Date")
        .reset_index(drop=True)
    )

    if df.empty:
        raise ValueError(f"No usable price rows found for {symbol}.")

    return df


def fetch_latest_data(
    symbol: str, lookback_rows: int = LOOKBACK_DAYS
) -> pd.DataFrame:
    """Return the latest completed daily rows for model inference."""
    # '6mo' is a supported yfinance period and gives us enough trading rows.
    df = fetch_stock_data(symbol, period="6mo")

    if len(df) < lookback_rows:
        raise ValueError(
            f"{symbol} has only {len(df)} rows; need {lookback_rows}."
        )

    return df.tail(lookback_rows).copy()