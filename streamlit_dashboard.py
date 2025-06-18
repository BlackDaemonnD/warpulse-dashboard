
import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

CSV_FILE = "warpulse_trades.csv"
REFRESH_INTERVAL = 60  # seconds

# Load and process trade data
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df['Time'] = pd.to_datetime(df['Time'])
        return df
    return pd.DataFrame(columns=["Time", "Symbol", "Direction", "Entry Price", "SL", "TP", "Lot"])

# Calculate equity curve based on dummy profit
def calculate_equity(df, start_balance=10000, profit_per_trade=100):
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df['Equity'] = start_balance + df.index * profit_per_trade
    return df

# Dashboard layout
st.set_page_config(page_title="WarPulse EA Dashboard", layout="wide")
st.title("📊 WarPulse EA Live Dashboard")

# Bot status
status_placeholder = st.empty()
last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
status_placeholder.success(f"🟢 Bot is ONLINE | Last checked: {last_updated}")

# Countdown to next refresh
countdown_placeholder = st.empty()
for remaining in range(REFRESH_INTERVAL, 0, -1):
    countdown_placeholder.info(f"⏱ Refreshing in {remaining} seconds...")
    time.sleep(1)

# Load data
df = load_data()
if df.empty:
    st.warning("No trade data available yet.")
else:
    # Show trade stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trades", len(df))
    with col2:
        win_rate = (len(df[df['Direction'] == 'BUY']) / len(df) * 100) if len(df) > 0 else 0
        st.metric("Buy Ratio", f"{win_rate:.2f}%")
    with col3:
        st.metric("Tracked Symbols", df['Symbol'].nunique())

    # Show live trade log
    st.subheader("📋 Recent Trade Log")
    st.dataframe(df.sort_values(by="Time", ascending=False), use_container_width=True)

    # Equity chart
    equity_df = calculate_equity(df)
    st.subheader("📈 Simulated Equity Curve")
    st.line_chart(equity_df.set_index("Time")["Equity"])

    # Export
    st.download_button("📥 Download Trade Log as CSV", df.to_csv(index=False), "warpulse_trades.csv")

# Footer
st.caption("Built by Segun's WarPulse EA 🧠")
