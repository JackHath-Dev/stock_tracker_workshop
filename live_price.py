# Basic live stock tracker

import time
from datetime import datetime

import yfinance as yf


def stream_price(ticker_symbol: str, interval: int = 5):
    print(f"Starting price stream for {ticker_symbol}")
    
    try:
        while True:
            ticker = yf.Ticker(ticker=ticker_symbol)
            price = ticker.fast_info["last_price"]
            timestamp = datetime.now().strftime("%H:%M:%S")

            print(f"[{timestamp}] {ticker_symbol}: ${price:.2f}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStream stopped.")

if __name__ == "__main__":
    stream_price("BTC-GBP", interval=5)

