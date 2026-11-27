from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.animation import FuncAnimation

TICKER = "BTC-USD"

# 1. Fetch & convert to UK time
LOCAL_TZ = ZoneInfo("Europe/London")
hist = yf.Ticker(TICKER).history(period="1d", interval="1m")
hist.index = hist.index.tz_convert(LOCAL_TZ)

times = list(hist.index)
prices = list(hist["Close"])

# 2. Initialize plot & 24-hour window
fig, ax = plt.subplots(figsize=(11, 5))
line, = ax.plot(times, prices)
ax.set_xlim(times[0], datetime.now(LOCAL_TZ) + timedelta(hours=1))

# 3. Update function for live tracking
def update(frame):
    try:
        price = yf.Ticker(TICKER).fast_info["last_price"]
        now = datetime.now(LOCAL_TZ)
        times.append(now); prices.append(price)
        print(price)

        times.pop(0)
        prices.pop(0)
        
        line.set_data(times, prices)
        ax.set_xlim(times[0], now + timedelta(hours=1))
        ax.relim()
        ax.autoscale_view(scalex=False, scaley=True)
    except Exception as e:
        print(f"Skipped tick: {e}")
    return line,

ani = FuncAnimation(fig, update, interval=10000)
plt.show()

