import pandas as pd

def simulate_trading_strategy(df, initial_capital=10000, risk_per_trade=0.02):
    """
    Simulate the trading strategy using the generated buy and sell signals with a 2:1 risk-reward ratio.
    
    Args:
    - df (DataFrame): The DataFrame containing the trading data, indicators, and signals.
    - initial_capital (float): The starting capital for the trading simulation.
    - risk_per_trade (float): The percentage of capital to risk per trade (e.g., 0.02 for 2%).
    
    Returns:
    - final_capital (float): The final capital after simulating the trading strategy.
    - trades_df (DataFrame): A DataFrame with the details of executed trades.
    """

    # Initialize variables
    capital = initial_capital
    position = None  # No position at the start
    entry_price = 0  # Price at which a position is entered
    units = 0  # Number of units to trade
    trades = []  # List to store trade details

    # Loop through the DataFrame to simulate the trades
    for index, row in df.iterrows():
        risk_amount = capital * risk_per_trade
        
        if 'Buy_Signal' in df.columns and row['Buy_Signal'] and position != 'long':
            # If a buy signal is detected and we're not already in a long position
            if position == 'short':
                # Close the short position
                capital += units * (entry_price - row['close'])
                trades.append({'timestamp': row['timestamp'], 'type': 'cover', 'price': row['close'], 'capital': capital})
            
            # Determine number of units to buy based on the risk amount and recent swing low
            entry_price = row['close']
            recent_swing_low = df.loc[:index, 'Swing_Low'].last_valid_index()
            if recent_swing_low is not None:
                stop_loss = df.at[recent_swing_low, 'low'] * 0.95  # Allow more room for fluctuation
                take_profit = entry_price + 2 * (entry_price - stop_loss)  # 2:1 risk-reward ratio
                if stop_loss < entry_price:  # Ensure the stop loss is below the entry price
                    units = risk_amount / (entry_price - stop_loss)
                    position = 'long'
                    trades.append({'timestamp': row['timestamp'], 'type': 'buy', 'price': entry_price, 'units': units, 'capital': capital, 'stop_loss': stop_loss, 'take_profit': take_profit})

        elif 'Sell_Signal' in df.columns and row['Sell_Signal'] and position != 'short':
            # If a sell signal is detected and we're not already in a short position
            if position == 'long':
                # Close the long position
                capital += units * (row['close'] - entry_price)
                trades.append({'timestamp': row['timestamp'], 'type': 'sell', 'price': row['close'], 'capital': capital})
            
            # Determine number of units to sell based on the risk amount and recent swing high
            entry_price = row['close']
            recent_swing_high = df.loc[:index, 'Swing_High'].last_valid_index()
            if recent_swing_high is not None:
                stop_loss = df.at[recent_swing_high, 'high'] * 1.05  # Allow more room for fluctuation
                take_profit = entry_price - 2 * (stop_loss - entry_price)  # 2:1 risk-reward ratio
                if stop_loss > entry_price:  # Ensure the stop loss is above the entry price
                    units = risk_amount / (stop_loss - entry_price)
                    position = 'short'
                    trades.append({'timestamp': row['timestamp'], 'type': 'sell_short', 'price': entry_price, 'units': units, 'capital': capital, 'stop_loss': stop_loss, 'take_profit': take_profit})
        
        # Check if stop loss or take profit is hit
        if position == 'long':
            if row['low'] <= stop_loss:
                # Hit stop loss on a long position
                capital -= units * (entry_price - stop_loss)
                trades.append({'timestamp': row['timestamp'], 'type': 'stop_loss', 'price': stop_loss, 'capital': capital})
                position = None
                units = 0
            elif row['high'] >= take_profit:
                # Hit take profit on a long position
                capital += units * (take_profit - entry_price)
                trades.append({'timestamp': row['timestamp'], 'type': 'take_profit', 'price': take_profit, 'capital': capital})
                position = None
                units = 0
        
        elif position == 'short':
            if row['high'] >= stop_loss:
                # Hit stop loss on a short position
                capital -= units * (stop_loss - entry_price)
                trades.append({'timestamp': row['timestamp'], 'type': 'stop_loss', 'price': stop_loss, 'capital': capital})
                position = None
                units = 0
            elif row['low'] <= take_profit:
                # Hit take profit on a short position
                capital += units * (entry_price - take_profit)
                trades.append({'timestamp': row['timestamp'], 'type': 'take_profit', 'price': take_profit, 'capital': capital})
                position = None
                units = 0

    # Convert trades to a DataFrame
    trades_df = pd.DataFrame(trades)
    
    # Calculate final capital
    final_capital = capital

    return final_capital, trades_df