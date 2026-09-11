import requests
import pandas as pd
from datetime import datetime

def fetch_crypto_data(coin_id: str, days: int = 365) -> pd.DataFrame:
    """
    Fetches historical daily price data for a given cryptocurrency from CoinGecko.
    """
    print(f"Fetching {days} days of data for {coin_id}...")
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': str(days),
        'interval': 'daily'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    prices = data.get('prices', [])
    
    if not prices:
        raise ValueError(f"No price data found for {coin_id}")
        
    # Prices are returned as [timestamp, price]
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    # Convert timestamp to datetime
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)
    df.drop('timestamp', axis=1, inplace=True)
    
    return df

def analyze_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes the price data to calculate daily returns, moving averages, volatility, Bollinger Bands, and RSI.
    """
    import numpy as np
    
    print("Analyzing data...")
    # Daily Returns
    df['daily_return'] = df['price'].pct_change()
    
    # Moving Averages (7-day and 30-day)
    df['ma_7'] = df['price'].rolling(window=7).mean()
    df['ma_30'] = df['price'].rolling(window=30).mean()
    
    # Volatility (30-day rolling standard deviation of daily returns)
    df['volatility_30d'] = df['daily_return'].rolling(window=30).std()
    
    # Bollinger Bands (20-day SMA, +/- 2 std dev)
    df['ma_20'] = df['price'].rolling(window=20).mean()
    df['bb_std'] = df['price'].rolling(window=20).std()
    df['bb_upper'] = df['ma_20'] + (df['bb_std'] * 2)
    df['bb_lower'] = df['ma_20'] - (df['bb_std'] * 2)
    
    # RSI (Relative Strength Index - 14 days)
    delta = df['price'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi_14'] = 100 - (100 / (1 + rs))
    
    return df

def export_to_csv(df: pd.DataFrame, coin_id: str) -> str:
    """
    Exports the DataFrame to a CSV file in the data/ directory.
    """
    import os
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    filename = f"data/{coin_id}_analysis_{datetime.now().strftime('%Y%m%d')}.csv"
    print(f"Exporting data to {filename}...")
    df.to_csv(filename)
    return filename
