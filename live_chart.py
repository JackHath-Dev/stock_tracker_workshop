# Live updating chart - Fourth section
# Will act funky if market shut

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.animation import FuncAnimation

TICKER = "AAPL"
POLL_INTERVAL = 10000  # 10 seconds
LOCAL_TZ = ZoneInfo("Europe/London")  # Change to your local timezone

# Fetching historical data
print(f"Fetching 24-hour historical data for {TICKER}...")
hist = yf.Ticker(TICKER).history(period="2d", interval="1m")
hist.index = hist.index.tz_convert(LOCAL_TZ)  # Convert to local timezone
times = list(hist.index)
prices = list(hist["Close"])

# Setting up graph
fig, ax = plt.subplots(figsize=(11, 5))
line, = ax.plot(times, prices)

# Formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=LOCAL_TZ))
ax.set_title(f"{TICKER} 24-Hour Live Tracker", fontsize=14, fontweight="bold")
ax.set_ylabel("Price (USD)")
ax.grid(True, linestyle="--", alpha=0.3)
fill = ax.fill_between(times, prices, min(prices), color="#00ff88", alpha=0.15)

# Maintains 24 hour window
window_end = times[-1] + timedelta(hours=1)
window_start = window_end - timedelta(hours=24)
ax.set_xlim(window_start, window_end)

# Update function
def update(frame):
    global fill
    try:
        # Last price
        price = yf.Ticker(TICKER).fast_info["last_price"]
        now = datetime.now(LOCAL_TZ)

        # Append live point and drop any data older than 24 hours
        times.append(now)
        prices.append(price)
        cutoff = now - timedelta(hours=23)
        while times and times[0] < cutoff:
            times.pop(0)
            prices.pop(0)

        line.set_data(times, prices)

        fill.remove()
        fill = ax.fill_between(times, prices, min(prices), color="#00ff88", alpha=0.15)

        # Slide the 24-hour window forward smoothly while keeping 1 hour of headroom
        ax.set_xlim(times[0], now + timedelta(hours=1))

        # Autoscale ONLY the y-axis (scalex=False prevents x-axis zooming)
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)

        ax.set_title(
            f"{TICKER} Live Price: ${price:,.2f}  (Updated: {now.strftime('%H:%M:%S')})",
            fontsize=14,
            fontweight="bold"
        )
    except Exception as e:
        print(f"Fetch error (skipping tick): {e}")

    return line,

# Graph acts as a repeating animation
ani = FuncAnimation(fig, update, interval=POLL_INTERVAL, cache_frame_data=False)
plt.tight_layout()
plt.show()