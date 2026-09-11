# Crypto Market Analysis Tool

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![CoinGecko API](https://img.shields.io/badge/API-CoinGecko-yellow.svg)
![Binance API](https://img.shields.io/badge/API-Binance_WebSockets-black.svg)

## Project Overview

The **Crypto Market Analysis Tool** is an end-to-end Python application designed to extract, analyze, and visualize historical cryptocurrency market data.

This project demonstrates core competencies in:
- **Data Engineering**: Historical data extraction via the public **CoinGecko REST API** and real-time streaming via the **Binance WebSocket API**.
- **Data Analysis (Data Science)**: Time-series data manipulation, calculating daily returns, moving averages (7-day and 30-day), and rolling volatility using **Pandas**.
- **Data Visualization**: Building a comprehensive, interactive web dashboard using **Streamlit** and **Plotly**.
- **Software Engineering**: Modular code structure, clear separation of concerns, and reproducible environments.

---

## Features

1. **Automated Data Extraction**: A script capable of fetching the complete historical price data for any cryptocurrency listed on CoinGecko (e.g., Bitcoin, Ethereum).
2. **Analysis Pipelines (Pandas)**: 
    - Generation of standard financial indicators (MA7, MA30).
    - 30-day rolling standard deviation (Volatility).
    - Saving processed results in a structured format (`.csv`).
3. **Interactive Web Dashboard**:
    - Smooth, dark-mode user interface powered by Streamlit (TradingView style).
    - Interactive charts (Plotly) enabling specific timeframe zoom-ins.
    - Integrated sidebar controls to fetch new CoinGecko data and download CSVs directly from the UI.
4. **Advanced Technical Indicators**:
    - RSI (Relative Strength Index) calculated over a 14-day window.
    - Bollinger Bands (20-day SMA, +/- 2 Standard Deviations) for volatility analysis.
5. **Real-time Live Streaming (WebSockets)**:
    - Dedicated live trading simulation tab.
    - Real-time connection to the Binance public WebSocket API (`wss://stream.binance.com`).
    - Continuous plotting of live market trades.

---

## Project Structure

```text
Crypto_Market_Analysis_Tool/
│
├── data/                   # Auto-generated directory containing CSV exports (git-ignored)
├── analyzer.py             # Core logic: API requests and mathematical calculations (Pandas)
├── main.py                 # CLI entry point to generate new market analysis
├── dashboard.py            # Streamlit web application for data visualization & Live Stream
├── requirements.txt        # Project dependencies
├── .gitignore              # Files and directories ignored by Git
└── README.md               # Project documentation
```

---

## Setup & Usage

### Prerequisites
Make sure you have **Python** or **Anaconda/Miniconda** installed.

### 1. Install Dependencies
Open your terminal (or Anaconda Prompt) and navigate to the project directory:
```bash
git clone https://github.com/your_name/Crypto_Market_Analysis_Tool.git
cd Crypto_Market_Analysis_Tool
```

Install dependencies via Conda:
```bash
conda install pandas requests streamlit plotly websocket-client -c conda-forge -y
```
*(Or using pip: `pip install -r requirements.txt`)*

### 2. Generate Data
Use the main script to download and analyze the historical market data.
```bash
# Default analysis (Bitcoin, 365 days)
python main.py

# Custom analysis
python main.py --coin ethereum --days 180
```
*The resulting files will be automatically saved in the `data/` directory.*

### 3. Launch the Dashboard
To visualize your analysis and access the Live Stream, launch the local web application:
```bash
streamlit run dashboard.py
```
The dashboard will automatically open in your default web browser.

---

## Future Enhancements
- Integration of MACD and Fibonacci retracement levels.
- Real-time portfolio tracking and PnL calculation.
- Cloud deployment of the dashboard (AWS, Heroku, or Streamlit Cloud).