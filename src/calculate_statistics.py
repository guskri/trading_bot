import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the trade log CSV file
trade_log_df = pd.read_csv('trade_log.csv')

# Check for missing data and handle it
if trade_log_df.isnull().sum().sum() > 0:
    print("Warning: Missing data detected. Filling missing values with zero.")
    trade_log_df.fillna(0, inplace=True)  # Or you could drop rows with missing data using `trade_log_df.dropna(inplace=True)`

# Initialize lists to hold statistics
wins = []
losses = []

# Initialize variables for tracking consecutive wins and losses
current_win_streak = 0
current_loss_streak = 0
max_win_streak = 0
max_loss_streak = 0

# Initialize variables for tracking drawdown
max_drawdown = 0
initial_balance = 10000  # Starting balance
account_balance = initial_balance
peak_value = initial_balance 
btc_balance = 0

# Initialize a list to track portfolio values for drawdown calculation
portfolio_values = []
timestamps = []  # List to track timestamps for plotting

# Iterate over the trade log to calculate win/loss and update portfolio value
for i in range(len(trade_log_df)):
    action = trade_log_df.iloc[i]['Action']
    price = trade_log_df.iloc[i]['Price']
    position_size = trade_log_df.iloc[i]['Position Size']
    
    if action == 'Buy':
        if price > 0:  # Ensure price is not zero
            btc_balance = position_size
            account_balance -= btc_balance * price
            trade_log_df.at[i, 'USD Balance'] = account_balance
            trade_log_df.at[i, 'BTC Balance'] = btc_balance
    elif action == 'Sell' and btc_balance > 0:
        if price > 0 and position_size > 0:
            account_balance += btc_balance * price
            btc_balance = 0
            trade_log_df.at[i, 'USD Balance'] = account_balance
            trade_log_df.at[i, 'BTC Balance'] = btc_balance

            # Calculate profit in dollars and percentage
            buy_price = trade_log_df.iloc[i - 1]['Price']
            sell_price = trade_log_df.iloc[i]['Price']
            profit = (sell_price - buy_price) * position_size
            profit_pct = (sell_price - buy_price) / buy_price if buy_price != 0 else 0

            if profit > 0:
                wins.append((profit, profit_pct))
                current_win_streak += 1
                current_loss_streak = 0  # Reset loss streak
            else:
                losses.append((profit, profit_pct))
                current_loss_streak += 1
                current_win_streak = 0  # Reset win streak

            # Update max streaks
            max_win_streak = max(max_win_streak, current_win_streak)
            max_loss_streak = max(max_loss_streak, current_loss_streak)
    
    # Update the portfolio value and drawdown
    portfolio_value = account_balance + (btc_balance * price) if price > 0 else account_balance
    portfolio_values.append(portfolio_value)
    timestamps.append(trade_log_df.iloc[i]['Timestamp'])
    
    # Update peak value and drawdown
    if portfolio_value > peak_value:
        peak_value = portfolio_value
    
    drawdown = (peak_value - portfolio_value) / peak_value if peak_value != 0 else 0
    max_drawdown = max(max_drawdown, drawdown)

# Calculate final portfolio value from the last row of the trade log
final_portfolio_value = account_balance  # Final account balance after all trades

# Ensure final portfolio value accounts for any BTC held
if btc_balance > 0:
    final_portfolio_value = account_balance + (btc_balance * trade_log_df.iloc[-1]['Price'])

# Calculate key statistics in dollars and percentages
win_rate = len(wins) / (len(wins) + len(losses)) * 100 if (len(wins) + len(losses)) > 0 else 0
average_win_dollar = np.mean([win[0] for win in wins]) if wins else 0
average_loss_dollar = np.mean([loss[0] for loss in losses]) if losses else 0
average_win_pct = np.mean([win[1] for win in wins]) * 100 if wins else 0
average_loss_pct = np.mean([loss[1] for loss in losses]) * 100 if losses else 0
biggest_win_dollar = max(wins, key=lambda x: x[0])[0] if wins else 0
biggest_loss_dollar = min(losses, key=lambda x: x[0])[0] if losses else 0
biggest_win_pct = max(wins, key=lambda x: x[1])[1] * 100 if wins else 0
biggest_loss_pct = min(losses, key=lambda x: x[1])[1] * 100 if losses else 0
num_trades = len(wins) + len(losses)
num_wins = len(wins)
num_losses = len(losses)

# Print statistics in dollars and percentages
print(f"Initial balance: ${initial_balance}")
print(f"Final portfolio value: ${final_portfolio_value:.2f}")
print(f"Profit/Loss: ${final_portfolio_value - initial_balance:.2f} ({((final_portfolio_value - initial_balance) / initial_balance) * 100:.2f}%)")
print(f"Win rate: {win_rate:.2f}%")
print(f"Average win: ${average_win_dollar:.2f} ({average_win_pct:.2f}%)")
print(f"Average loss: ${average_loss_dollar:.2f} ({average_loss_pct:.2f}%)")
print(f"Biggest win: ${biggest_win_dollar:.2f} ({biggest_win_pct:.2f}%)")
print(f"Biggest loss: ${biggest_loss_dollar:.2f} ({biggest_loss_pct:.2f}%)")
print(f"Number of trades: {num_trades}")
print(f"Number of wins: {num_wins}")
print(f"Number of losses: {num_losses}")
print(f"Max consecutive wins: {max_win_streak}")
print(f"Max consecutive losses: {max_loss_streak}")
print(f"Max drawdown: {max_drawdown * 100:.2f}%")

# Plotting the portfolio value over time and saving it to a file
plt.figure(figsize=(14, 7))
plt.plot(timestamps, portfolio_values, label='Portfolio Value', color='blue', alpha=0.8)

# Marking Buy and Sell signals on the plot
buy_signals = trade_log_df[trade_log_df['Action'] == 'Buy']
sell_signals = trade_log_df[trade_log_df['Action'] == 'Sell']

plt.plot(buy_signals['Timestamp'], buy_signals['Price'], '^', markersize=10, color='g', lw=0, label='Buy Signal')
plt.plot(sell_signals['Timestamp'], sell_signals['Price'], 'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title('Portfolio Value Over Time with Buy and Sell Signals')
plt.xlabel('Date')
plt.ylabel('Portfolio Value (USD)')
plt.legend(loc='best')
plt.grid(True)

# Save the plot to a file instead of displaying it
plt.savefig('portfolio_value_plot.png')

print("Plot saved to 'portfolio_value_plot.png'.")
