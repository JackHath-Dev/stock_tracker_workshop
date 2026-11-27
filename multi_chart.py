# Multiple charts

from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.animation import FuncAnimation

SYMBOLS = ["BTC-USD", "ETH-USD", "XRP-USD"]
POLL_INTERVAL = 10000  # 10 seconds

data = {}
for sym in SYMBOLS:
    print(f"Fetching 24-hour historical data for {sym}...")
    hist = yf.Ticker(sym).history(period="1d", interval="1m")
    data[sym] = {
        "times": list(hist.index),
        "prices": list(hist["Close"])
    }

fig, axes = plt.subplots(len(SYMBOLS), 1, figsize=(11, 7), sharex=True)

if len(SYMBOLS) == 1:
    axes = [axes]

lines = {}
for ax, sym in zip(axes, SYMBOLS):
    line, = ax.plot(data[sym]["times"], data[sym]["prices"])
    lines[sym] = line

    ax.set_ylabel("Price (USD)")
    ax.set_title(f"{sym}", fontsize=14, fontweight="bold")


ref_tz = data[SYMBOLS[0]]["times"][-1].tzinfo
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=ref_tz))
now_init = datetime.now(ref_tz)
earliest_time = min(data[sym]["times"][0] for sym in SYMBOLS)
axes[-1].set_xlim(earliest_time, now_init + timedelta(hours=1))

def update(frame):
    try:
        # Batch-fetch all tickers in one request instead of looping HTTP calls
        tickers = yf.Tickers(" ".join(SYMBOLS))
        now = datetime.now(ref_tz)
        cutoff = now - timedelta(hours=23)

        for ax, sym in zip(axes, SYMBOLS):
            latest_price = tickers.tickers[sym].fast_info["last_price"]

            times = data[sym]["times"]
            prices = data[sym]["prices"]
            times.append(now)
            prices.append(latest_price)

            while times and times[0] < cutoff:
                times.pop(0)
                prices.pop(0)

            lines[sym].set_data(times, prices)

            # Rescale each panel's y-axis independently (Bitcoin is ~$90k, Solana is ~$200)
            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True)
            ax.set_title(
                f"{sym}: ${latest_price:,.2f}  (Updated: {now.strftime('%H:%M:%S')})",
                fontsize=11,
                fontweight="bold",
                loc="left",
            )

        # Slide the shared x-axis forward once for all stacked panels
        earliest_time = min(data[sym]["times"][0] for sym in SYMBOLS)
        axes[-1].set_xlim(earliest_time, now + timedelta(hours=1))

    except Exception as e:
        print(f"Batch fetch error (skipping tick): {e}")

    return list(lines.values())

ani = FuncAnimation(fig, update, interval=POLL_INTERVAL, cache_frame_data=False)
plt.tight_layout()
plt.show()