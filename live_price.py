# Basic live stock tracker - Third section

import time
from datetime import datetime

import yfinance as yf


# Function fetches current price and displays it every 5 seconds
def stream_price(ticker_symbol: str, interval: int = 5):
    print(f"Starting price stream for {ticker_symbol}")
    
    try:
        while True:
            ticker = yf.Ticker(ticker=ticker_symbol)
            # A ticker object can return varying information about the asset
            price = ticker.fast_info["last_price"]
            timestamp = datetime.now().strftime("%H:%M:%S")

            print(f"[{timestamp}] {ticker_symbol}: ${price:.2f}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStream stopped.")

if __name__ == "__main__":
    stream_price("BTC-USD", interval=5)