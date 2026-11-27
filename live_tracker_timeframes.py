from datetime import datetime
from zoneinfo import ZoneInfo

import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter, MaxNLocator

SYMBOLS = ["AAPL", "NVDA"]
COLORS = ["#00ccff", "#00ff88"]
TIMEFRAME = "5d"  # Options: "1h", "1d", "5d", "1mo", "6mo"
POLL_INTERVAL = 10000  # 10 seconds
LOCAL_TZ = ZoneInfo("Europe/London")

# Maps a human-friendly timeframe to (yfinance period, interval, max_points, label_format)
TIMEFRAME_CONFIG = {
    "1h":  {"period": "5d",  "interval": "1m",  "max_points": 60,  "fmt": "%H:%M"},
    "1d":  {"period": "5d",  "interval": "5m",  "max_points": 78,  "fmt": "%d %b %H:%M"},
    "5d":  {"period": "5d",  "interval": "15m", "max_points": 130, "fmt": "%d %b %H:%M"},
    "1mo": {"period": "1mo", "interval": "1h",  "max_points": 160, "fmt": "%d %b"},
    "6mo": {"period": "6mo", "interval": "1d",  "max_points": 130, "fmt": "%d %b '%y"},
}

cfg = TIMEFRAME_CONFIG[TIMEFRAME]

data = {}
for sym in SYMBOLS:
    print(f"Fetching {TIMEFRAME} baseline for {sym}...")
    hist = yf.Ticker(sym).history(period=cfg["period"], interval=cfg["interval"])
    hist = hist.tail(cfg["max_points"])
    hist.index = hist.index.tz_convert(LOCAL_TZ)

    data[sym] = {
        "labels": [ts.strftime(cfg["fmt"]) for ts in hist.index],
        "prices": list(hist["Close"]),
    }

plt.style.use("dark_background")
fig, axes = plt.subplots(len(SYMBOLS), 1, figsize=(11, 6.5), sharex=False)
if len(SYMBOLS) == 1:
    axes = [axes]

lines = {}
for ax, sym, color in zip(axes, SYMBOLS, COLORS):
    prices = data[sym]["prices"]
    labels = data[sym]["labels"]

    # Plot by sequential index (0, 1, 2...) to remove all market closure gaps
    line, = ax.plot(range(len(prices)), prices, color=color, linewidth=1.6)
    lines[sym] = line

    # Automatically map integer index positions -> formatted timestamp strings
    def make_formatter(sym_labels):
        def format_index(x, pos):
            idx = int(round(x))
            if 0 <= idx < len(sym_labels):
                return sym_labels[idx]
            return ""
        return FuncFormatter(format_index)

    ax.xaxis.set_major_formatter(make_formatter(labels))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=8, integer=True))
    ax.set_xlim(0, max(len(prices) + 3, 10))  # Slight right-side headroom for live ticks

    ax.set_ylabel("Price (USD)")
    ax.set_title(f"{sym} ({TIMEFRAME}) — Loading...", fontsize=11, fontweight="bold", loc="left")
    ax.grid(True, linestyle="--", alpha=0.3)

def update(frame):
    try:
        tickers = yf.Tickers(" ".join(SYMBOLS))
        now = datetime.now(LOCAL_TZ)
        now_label = now.strftime("%H:%M:%S")

        for ax, sym in zip(axes, SYMBOLS):
            latest_price = tickers.tickers[sym].fast_info["last_price"]
            labels = data[sym]["labels"]
            prices = data[sym]["prices"]

            labels.append(now_label)
            prices.append(latest_price)

            # Keep rolling window fixed at max_points
            if len(prices) > cfg["max_points"]:
                labels.pop(0)
                prices.pop(0)

            x_vals = range(len(prices))
            lines[sym].set_data(x_vals, prices)
            ax.set_xlim(0, len(prices) + 3)

            ax.relim()
            ax.autoscale_view(scalex=False, scaley=True)
            ax.set_title(
                f"{sym} ({TIMEFRAME}): ${latest_price:,.2f}  (Updated: {now_label})",
                fontsize=11,
                fontweight="bold",
                loc="left",
            )
    except Exception as e:
        print(f"Batch fetch error (skipping tick): {e}")

    return list(lines.values())

ani = FuncAnimation(fig, update, interval=POLL_INTERVAL, cache_frame_data=False)
plt.tight_layout()
plt.show()