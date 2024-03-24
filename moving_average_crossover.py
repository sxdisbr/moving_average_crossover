from datetime import timedelta
import yfinance as yf
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Fetch historical data for Bitcoin
btc = yf.Ticker("BTC-USD")
df = btc.history(period="1y", interval="1d")

# Ensure the data is sorted by date
df.sort_index(inplace=True)

# Find the last date in the DataFrame
last_date = df.index.max()

# Calculate the first date of the last month
first_date = (last_date - timedelta(days=30))

# Filter the DataFrame to include only the last month's data
df_last_month = df.loc[first_date:last_date]

short_window = 10
long_window = 20

# Calculate moving averages for the filtered last month's data
df_last_month['short_mavg'] = df_last_month['Close'].rolling(window=short_window, min_periods=1).mean()
df_last_month['long_mavg'] = df_last_month['Close'].rolling(window=long_window, min_periods=1).mean()

# Create signals for the filtered last month's data
df_last_month['signal'] = 0
df_last_month['signal'][short_window:] = np.where(df_last_month['short_mavg'][short_window:] > df_last_month['long_mavg'][short_window:], 1, 0)
df_last_month['positions'] = df_last_month['signal'].diff()

fig, ax = plt.subplots(figsize=(12, 6))

# Plot the closing price, short_mavg, long_mavg for the last month
df_last_month['Close'].plot(ax=ax, label='BTC Close', alpha=0.5)
df_last_month['short_mavg'].plot(ax=ax, label=f'Short {short_window}D MA', alpha=0.75)
df_last_month['long_mavg'].plot(ax=ax, label=f'Long {long_window}D MA', alpha=0.75)

# Highlight buy signals
ax.plot(df_last_month[df_last_month['positions'] == 1].index, 
         df_last_month['short_mavg'][df_last_month['positions'] == 1], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Highlight sell signals
ax.plot(df_last_month[df_last_month['positions'] == -1].index, 
         df_last_month['short_mavg'][df_last_month['positions'] == -1], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

# Define the date format
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('"%Y-%m-%d"'))

plt.title("Bitcoin Buy/Sell Signals")
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()