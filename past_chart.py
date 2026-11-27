# Past data on charts - Second section

import matplotlib.pyplot as plt
import yfinance as yf

ticker = yf.Ticker("AAPL")
df = ticker.history(period="6mo", interval="1d")

df.to_csv("AAPL_6mo.csv")  # Save to CSV for future reference
# pd.read_csv("AAPL_6mo.csv") # Read from CSV

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df.index, df["Close"], label="Close Price", linewidth=1.5)
plt.fill_between(df.index, df["Close"], df["Close"].min(), color='skyblue', alpha=0.4)
# or if you want to fill between the close price and 0
# plt.fill_between(df.index, df["Close"], color='skyblue', alpha=0.4)

# If you want to plot the 20-day SMA for example
df["SMA"] = df["Close"].rolling(window=20).mean()
ax.plot(df.index, df["SMA"], label="20-Day SMA", color='orange', linewidth=1.5) # Only shows after first 19 data points
# This can be changed if you fetch the first 7 months, but only plot the last 6 months

ax.set_title(f"{ticker.ticker} - 6-Month Price with 20-Day SMA", fontsize=14, fontweight="bold")
ax.set_ylabel("Price (USD)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()