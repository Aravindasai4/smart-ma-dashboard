import streamlit as st

st.set_page_config(layout="wide")
st.title("📊 Smart MA Dashboard (TradingView Powered)")

with st.form("chart_form"):
    tickers = st.multiselect(
        "Select stock tickers to display",
        ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL", "AMZN", "META"],
        ["AAPL", "TSLA"]
    )
    submitted = st.form_submit_button("📥 Submit")

if submitted:
    if not tickers:
        st.warning("Please select at least one stock.")
    else:
        for ticker in tickers:
            st.markdown(f"### 📈 {ticker} Chart")
            st.components.v1.html(f"""
            <div class="tradingview-widget-container">
              <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?locale=en#%7B%22symbol%22%3A%22NASDAQ%3A{ticker}%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A300%2C%22locale%22%3A%22en%22%2C%22dateRange%22%3A%22ytd%22%2C%22colorTheme%22%3A%22dark%22%2C%22trendLineColor%22%3A%22rgba(41%2C%2098%2C%20255%2C%201)%22%2C%22underLineColor%22%3A%22rgba(41%2C%2098%2C%20255%2C%200.3)%22%2C%22isTransparent%22%3Afalse%2C%22autosize%22%3Atrue%7D" 
              width="100%" height="300" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
            </div>
            """, height=320)
