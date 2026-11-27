# Past data - First section

import yfinance as yf

ticker = yf.Ticker("AAPL")

df = ticker.history(period="6mo", interval="1d")

# Or

data = yf.download(["AAPL", "BTC-USD"], period="1y", interval="1d")

# Handling the data

df = ticker.history(period="5d", interval="1h")

print(f"Shape (rows, columns): {df.shape}")
print(f"\nFirst 5 rows:\n{df.head()}")

print("\nSummary statistics:")
print(df[["Open", "High", "Low", "Close", "Volume"]].describe()) # Summarises and fetches statistics

closing_prices = df["Close"]
highest_price = df["High"].max()
lowest_price = df["Low"].min()

df["Pct_Change"] = df["Close"].pct_change() * 100
df["SMA_24"] = df["Close"].rolling(window=24).mean() # 24 last rows

print(df[["Close", "Pct_Change", "SMA_24"]].tail(5))