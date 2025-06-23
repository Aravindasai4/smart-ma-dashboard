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
<div class="tradingview-widget-container" style="margin-top:10px">
  <div id="tradingview_{ticker}" />
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%",
      "height": 500,
      "symbol": "NASDAQ:{ticker}",
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",  // Candlestick style
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": false,
      "container_id": "tradingview_{ticker}"
    }});
  </script>
</div>
""", height=520)

