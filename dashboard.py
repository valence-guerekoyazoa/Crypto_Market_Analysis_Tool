import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import os
import json
import time

# Try to import websocket, handle if not installed yet
try:
    import websocket
    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False

st.set_page_config(page_title="Crypto Market Dashboard", layout="wide")

st.title("📈 Crypto Market Analysis Dashboard")

# Create tabs
tab_hist, tab_live = st.tabs(["📊 Historical Analysis", "🔴 Live Trading Simulation"])

# ==========================================
# TAB 1: HISTORICAL ANALYSIS
# ==========================================
with tab_hist:
    st.header("Historical Market Data & Technical Indicators")
    
    # 1. File Selection
    csv_files = glob.glob(os.path.join("data", "*_analysis_*.csv"))
    # Sort files by modification time, newest first
    csv_files.sort(key=os.path.getmtime, reverse=True)

    if not csv_files:
        st.warning("No analysis files found. Please run `python main.py` first to generate data.")
    else:
        selected_file = st.sidebar.selectbox("Select an analysis file", csv_files)

        @st.cache_data
        def load_data(file_path):
            df = pd.read_csv(file_path, parse_dates=['date'])
            return df

        df = load_data(selected_file)
        
        # --- Button to download or delete the current CSV ---
        csv_data = df.to_csv(index=False).encode('utf-8')
        filename_only = os.path.basename(selected_file)
        
        dl_col, del_col = st.sidebar.columns(2)
        with dl_col:
            st.download_button(
                label="💾 Download",
                data=csv_data,
                file_name=filename_only,
                mime='text/csv',
            )
        with del_col:
            if st.button("🗑️ Delete"):
                st.session_state['confirm_delete'] = selected_file
                st.rerun()
                
        # --- Confirmation logic ---
        if st.session_state.get('confirm_delete') == selected_file:
            st.sidebar.warning(f"Delete {filename_only}?")
            c1, c2 = st.sidebar.columns(2)
            with c1:
                if st.button("✔️ Yes"):
                    try:
                        os.remove(selected_file)
                        st.session_state['confirm_delete'] = None
                        st.sidebar.success("Deleted!")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"Error: {e}")
            with c2:
                if st.button("❌ No"):
                    st.session_state['confirm_delete'] = None
                    st.rerun()

    # --- Form to fetch new data ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Generate New Data")
    new_coin = st.sidebar.text_input("CoinGecko ID (e.g. bitcoin, solana)", value="bitcoin")
    new_days = st.sidebar.number_input("Number of days", min_value=1, max_value=3650, value=365)
    
    if st.sidebar.button("Run Analysis"):
        with st.spinner(f"Fetching data for {new_coin}..."):
            import sys
            # Add current path to import analyzer if needed
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            from analyzer import fetch_crypto_data, analyze_data, export_to_csv
            try:
                raw_df = fetch_crypto_data(new_coin, int(new_days))
                analyzed_df = analyze_data(raw_df)
                export_to_csv(analyzed_df, new_coin)
                st.sidebar.success(f" Data for {new_coin} successfully generated!")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error : {e}")
                
    if csv_files:
        # 2. Dynamic Title & KPIs
        coin_name = os.path.basename(selected_file).split('_analysis_')[0].capitalize()
        st.subheader(f"Asset: {coin_name}")
        
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest Price (USD)", f"${latest['price']:,.2f}", f"{(latest['price'] - previous['price']):,.2f}")
        col2.metric("Daily Return", f"{latest['daily_return'] * 100:.2f}%", f"{(latest['daily_return'] - previous['daily_return']) * 100:.2f}%")
        
        # Format RSI and BB gracefully if they exist
        rsi_val = f"{latest['rsi_14']:.2f}" if 'rsi_14' in latest and pd.notna(latest['rsi_14']) else "N/A"
        col3.metric("RSI (14D)", rsi_val)
        col4.metric("Volatility 30D", f"{latest['volatility_30d'] * 100:.2f}%")

        st.markdown("---")

        # 3. Main Chart (Price, MA, Bollinger Bands) & RSI
        st.subheader("Price Action, Bollinger Bands & RSI")
        
        # Create subplots: 2 rows, shared x-axis
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.05, row_heights=[0.7, 0.3])

        # Row 1: Price and Bands
        fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines', name='Price', line=dict(color='blue', width=2)), row=1, col=1)
        
        if 'bb_upper' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['bb_upper'], line=dict(color='lightgrey', width=1), name='BB Upper'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['date'], y=df['bb_lower'], line=dict(color='lightgrey', width=1), fill='tonexty', fillcolor='rgba(200,200,200,0.2)', name='BB Lower'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['date'], y=df['ma_20'], line=dict(color='orange', width=1, dash='dot'), name='SMA 20'), row=1, col=1)

        # Row 2: RSI
        if 'rsi_14' in df.columns:
            fig.add_trace(go.Scatter(x=df['date'], y=df['rsi_14'], line=dict(color='purple', width=2), name='RSI 14'), row=2, col=1)
            # Add overbought/oversold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        fig.update_layout(height=600, hovermode="x unified", template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: LIVE TRADING SIMULATION
# ==========================================
with tab_live:
    st.header("Live Market Stream")
    
    if not WS_AVAILABLE:
        st.error("The `websocket-client` library is not installed. Please run: `pip install websocket-client`")
    else:
        symbol = st.selectbox("Select Trading Pair", ["btcusdt", "ethusdt", "solusdt"])
        
        st.markdown("This connects directly to the public Binance WebSocket stream to fetch real-time trades.")
        
        start_stream = st.button("Start Live Stream")
        
        if start_stream:
            placeholder = st.empty()
            
            try:
                # Basic implementation of a websocket stream consumption in Streamlit
                ws = websocket.create_connection(f"wss://stream.binance.com:9443/ws/{symbol}@trade")
                
                # We will fetch trades continuously until the user stops the app
                st.info("Streaming in progress... (Click 'Stop' in top right to cancel)")
                
                prices = []
                while True:
                    result = ws.recv()
                    data = json.loads(result)
                    price = float(data['p'])
                    prices.append(price)
                    
                    # Keep only the last 100 prices to avoid memory overflow in the chart
                    if len(prices) > 100:
                        prices.pop(0)
                    
                    with placeholder.container():
                        st.metric(label=f"Current Price ({symbol.upper()})", value=f"${price:,.2f}")
                        
                        # Plot small line chart of recent live prices
                        fig_live = go.Figure(data=go.Scatter(y=prices, mode='lines+markers', line=dict(color='red')))
                        fig_live.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark")
                        st.plotly_chart(fig_live, use_container_width=True)
                        
                ws.close()
                st.success("Stream finished.")
                
            except Exception as e:
                st.error(f"WebSocket connection error: {e}")
