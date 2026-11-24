# Past data on charts

import matplotlib.pyplot as plt
import yfinance as yf

ticker = yf.Ticker("AAPL")
df = ticker.history(period="6mo", interval="1d")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df.index, df["Close"], label="Close Price")

ax.set_title("Apple - 6-Month Price")
ax.set_ylabel("Price (USD)")
ax.legend()

plt.tight_layout()
plt.show()