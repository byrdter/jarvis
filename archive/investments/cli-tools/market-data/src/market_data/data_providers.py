"""
Data providers for market data.

Supports multiple data sources:
- Alpaca API (preferred): 7+ years historical data, 200 calls/min
- yfinance (fallback): ~250 days max, no API key needed
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class AlpacaProvider:
    """Alpaca API data provider."""

    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")

        if not self.api_key or not self.secret_key:
            raise ValueError("Alpaca API keys not found in environment variables")

        # Import here to avoid dependency if not using Alpaca
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame
        from alpaca.data.enums import DataFeed

        # Use IEX feed for free tier (SIP requires paid subscription)
        self.client = StockHistoricalDataClient(
            self.api_key,
            self.secret_key,
            raw_data=False,
            url_override=None
        )
        self.StockBarsRequest = StockBarsRequest
        self.TimeFrame = TimeFrame
        self.DataFeed = DataFeed

    def get_history(self, symbol: str, days: int = 200) -> pd.DataFrame:
        """
        Get historical price data from Alpaca.

        Args:
            symbol: Stock/ETF ticker symbol
            days: Number of trading days of historical data

        Returns:
            DataFrame with OHLCV data
        """
        end_date = datetime.now()
        # Convert trading days to calendar days (~1.4x accounting for weekends/holidays)
        calendar_days = int(days * 1.5)
        start_date = end_date - timedelta(days=calendar_days)

        request_params = self.StockBarsRequest(
            symbol_or_symbols=symbol.upper(),
            timeframe=self.TimeFrame.Day,
            start=start_date,
            end=end_date,
            feed=self.DataFeed.IEX  # Use IEX feed for free tier
        )

        bars = self.client.get_stock_bars(request_params)

        # Convert to DataFrame
        df = bars.df

        if df.empty:
            raise ValueError(f"No data returned for {symbol}")

        # Reset index to get symbol and timestamp as columns
        df = df.reset_index()

        # Set timestamp as index
        df = df.set_index('timestamp')

        # Rename columns to match yfinance format
        df = df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume',
            'vwap': 'VWAP',
            'trade_count': 'Trade_Count'
        })

        # Keep only the columns we need
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

        return df

    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price and basic info from Alpaca.

        Args:
            symbol: Stock/ETF ticker symbol

        Returns:
            Dictionary with current price data
        """
        # Get latest bar data
        hist = self.get_history(symbol, days=5)  # Just need recent data

        if hist.empty:
            raise ValueError(f"No data found for {symbol}")

        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) > 1 else latest

        # Calculate 52-week high/low from longer history
        hist_52w = self.get_history(symbol, days=365)

        return {
            "symbol": symbol.upper(),
            "current_price": float(latest['Close']),
            "previous_close": float(prev['Close']),
            "open": float(latest['Open']),
            "day_high": float(latest['High']),
            "day_low": float(latest['Low']),
            "volume": int(latest['Volume']),
            "52_week_high": float(hist_52w['High'].max()),
            "52_week_low": float(hist_52w['Low'].min()),
            "data_source": "Alpaca (15 min delay)",
        }


class YFinanceProvider:
    """yfinance data provider (fallback)."""

    def __init__(self):
        # Import here to keep it optional
        import yfinance as yf
        self.yf = yf

    def get_history(self, symbol: str, days: int = 200) -> pd.DataFrame:
        """
        Get historical price data from yfinance.

        Args:
            symbol: Stock/ETF ticker symbol
            days: Number of days of historical data

        Returns:
            DataFrame with OHLCV data
        """
        ticker = self.yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 30)

        hist = ticker.history(start=start_date, end=end_date)

        if hist.empty:
            raise ValueError(f"No data found for {symbol}")

        return hist

    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price and basic info from yfinance.

        Args:
            symbol: Stock/ETF ticker symbol

        Returns:
            Dictionary with current price data
        """
        ticker = self.yf.Ticker(symbol)
        info = ticker.info

        return {
            "symbol": symbol.upper(),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "open": info.get("open") or info.get("regularMarketOpen"),
            "day_high": info.get("dayHigh") or info.get("regularMarketDayHigh"),
            "day_low": info.get("dayLow") or info.get("regularMarketDayLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            "data_source": "Yahoo Finance (15-20 min delay)",
        }


def get_data_provider():
    """
    Get the configured data provider.

    Returns:
        Data provider instance (Alpaca or yfinance)
    """
    source = os.getenv("DATA_SOURCE", "alpaca").lower()

    if source == "alpaca":
        try:
            return AlpacaProvider()
        except (ValueError, ImportError) as e:
            print(f"Warning: Could not initialize Alpaca provider ({e}). Falling back to yfinance.")
            return YFinanceProvider()
    else:
        return YFinanceProvider()
