import pandas as pd
import numpy as np
from money_management import apply_risk_management

# Load data from CSV file
df = pd.read_csv('./data/btc_usdt_5m_data.csv')

# Ensure the timestamp column is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Sort data by timestamp
df = df.sort_values('timestamp')

# Calculate EMAs
short_window = 10  # Short-term EMA window
long_window = 43   # Long-term EMA window
df['EMA_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
df['EMA_long'] = df['close'].ewm(span=long_window, adjust=False).mean()

# Generate signals: 1 for buy, 0 for hold
df['signal'] = np.where(df['EMA_short'] > df['EMA_long'], 1, 0)
df['position'] = df['signal'].diff()

# Calculate True Range (TR) and ATR
df['High-Low'] = df['high'] - df['low']
df['High-Close'] = np.abs(df['high'] - df['close'].shift(1))
df['Low-Close'] = np.abs(df['low'] - df['close'].shift(1))
df['TR'] = df[['High-Low', 'High-Close', 'Low-Close']].max(axis=1)
df['ATR'] = df['TR'].rolling(window=14).mean()  # 14-period ATR

# Fill NaN values that could be produced by rolling calculations
df['ATR'] = df['ATR'].bfill()  # Use bfill() to fill NaN values

# Backtesting the strategy
initial_balance = 10000  # Starting balance in USD
btc_balance = 0
usd_balance = initial_balance
trade_log = []

# Simulate trading
for i in range(len(df)):
    if df['position'].iloc[i] == 1:  # Buy signal
        btc_balance = usd_balance / df['close'].iloc[i]
        usd_balance = 0
        trade_log.append(('Buy', df['timestamp'].iloc[i], df['close'].iloc[i], btc_balance, usd_balance))
    elif df['position'].iloc[i] == -1 and btc_balance > 0:  # Sell signal, only if holding BTC
        usd_balance = btc_balance * df['close'].iloc[i]
        btc_balance = 0
        trade_log.append(('Sell', df['timestamp'].iloc[i], df['close'].iloc[i], btc_balance, usd_balance))

# Convert trade log to a DataFrame
trade_log_df = pd.DataFrame(trade_log, columns=['Action', 'Timestamp', 'Price', 'BTC Balance', 'USD Balance'])

# Apply money management with dynamic stop-loss based on ATR
risk_per_trade = 0.25  # Example: Risk 2% of the account per trade
trade_log_df = apply_risk_management(trade_log_df, df, initial_balance, risk_per_trade)

# Save trade log to a CSV file
trade_log_df.to_csv('trade_log.csv', index=False)

print("Trade log with money management saved to 'trade_log.csv'.")
