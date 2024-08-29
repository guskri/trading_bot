import ccxt
import pandas as pd
from datetime import datetime, timedelta

# Initialize the Binance exchange
exchange = ccxt.binance()

# Define the cryptocurrency pair and timeframe
symbol = 'BTC/USDT'
timeframe = '5m'  # 5-minute timeframe
since = exchange.parse8601('2022-08-01T00:00:00Z')  # Start date

# Initialize an empty list to hold the data
all_data = []

# Fetch historical data in chunks
while True:
    data = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
    if not data:
        break  # If no data is returned, exit the loop
    
    all_data.extend(data)  # Add the fetched data to the list
    since = data[-1][0] + 1  # Move to the next time period (last timestamp + 1ms)
    
    # Optional: Print progress
    print(f"Fetched {len(data)} records, total so far: {len(all_data)}")

# Convert the data into a pandas DataFrame
df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# Convert the timestamp to a readable datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(f"Total records fetched: {len(df)}")
print(df.head())  # Display the first few rows of the data

# Save the data to a CSV file (optional)
df.to_csv('./data/btc_usdt_5m_data.csv', index=False)
