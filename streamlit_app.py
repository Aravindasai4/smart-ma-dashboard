import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Smart MA Dashboard (Alpha Vantage Powered)")

API_KEY = "9WHK4JM9F91A4Y9S"  # Replace with your real API key if rotating later

with st.form("chart_form"):
    ticker = st.selectbox("Select a stock", ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META"], index=0)
    submitted = st.form_submit_button("📥 Submit")

def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        return None

    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "6. volume": "Volume"
    })
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def add_moving_averages(df):
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    df["MA_200"] = df["Close"].rolling(window=200).mean()
    return df

if submitted:
    st.markdown(f"### 📈 {ticker} — Candlestick + 20 & 200 MA")
    with st.spinner("Fetching data..."):
        df = get_stock_data(ticker)

    if df is None:
        st.error("⚠️ Could not retrieve data. API may be rate-limited or symbol is incorrect.")
    else:
        df = add_moving_averages(df)

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlestick"
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["MA_20"],
            line=dict(color="blue", width=1),
            name="20-Day MA"
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["MA_200"],
            line=dict(color="orange", width=1),
            name="200-Day MA"
        ))
        fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=600)
        st.plotly_chart(fig, use_container_width=True)
