import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("📊 Smart MA Dashboard")

# --- Form UI ---
with st.form("ma_form"):
    tickers = st.multiselect("Select stock tickers", ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"], ["AAPL", "TSLA"])
    ma_options = st.multiselect("Select moving averages", [20, 50, 100, 200], [20, 50, 100, 200])
    submitted = st.form_submit_button("📥 Submit")

@st.cache_data
def get_data(ticker, period="1y"):
    df = yf.download(ticker, period=period)
    return df

if submitted:
    if not tickers or not ma_options:
        st.warning("Please select at least one ticker and one MA.")
    else:
        for ticker in tickers:
            df = get_data(ticker)
            for ma in ma_options:
                df[f"MA_{ma}"] = df["Close"].rolling(ma).mean()
            df.dropna(inplace=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close", line=dict(color="black")))
            for ma in ma_options:
                fig.add_trace(go.Scatter(x=df.index, y=df[f"MA_{ma}"], name=f"{ma}-day MA"))
            fig.update_layout(title=f"{ticker} with Moving Averages", xaxis_title="Date", yaxis_title="Price")
            st.plotly_chart(fig, use_container_width=True)
