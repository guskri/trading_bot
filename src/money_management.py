import pandas as pd  # Add this line to import pandas

def apply_risk_management(trade_log_df, price_data, account_balance, risk_per_trade):
    # Initialize the position size and stop-loss columns with appropriate data types
    trade_log_df['Position Size'] = 0.0
    trade_log_df['Stop Loss'] = 0.0

    for i in range(len(trade_log_df)):
        if trade_log_df['Action'].iloc[i] == 'Buy':
            entry_price = trade_log_df['Price'].iloc[i]
            
            # Calculate stop loss using ATR
            atr_row = price_data[price_data['timestamp'] == trade_log_df['Timestamp'].iloc[i]]
            if not atr_row.empty and not pd.isna(atr_row['ATR'].values[0]):
                atr = atr_row['ATR'].values[0]
                stop_loss_price = entry_price - (atr * 2)  # Example: Stop loss 2 ATR below entry
            else:
                stop_loss_price = entry_price * 0.98  # Default stop loss as 2% below entry if ATR is missing

            position_size = calculate_position_size(account_balance, risk_per_trade, entry_price, stop_loss_price)
            trade_log_df.at[i, 'Position Size'] = position_size
            trade_log_df.at[i, 'Stop Loss'] = stop_loss_price

            account_balance -= position_size * entry_price  # Adjust account balance for buying BTC

        elif trade_log_df['Action'].iloc[i] == 'Sell':
            position_size = trade_log_df['Position Size'].iloc[i - 1]  # Use the previous buy position size
            trade_log_df.at[i, 'Position Size'] = position_size

            account_balance += position_size * trade_log_df['Price'].iloc[i]  # Adjust account balance for selling BTC

    return trade_log_df

def calculate_position_size(account_balance, risk_per_trade, entry_price, stop_loss_price):
    risk_amount = account_balance * (risk_per_trade / 100)  # Amount of USD to risk
    stop_loss_distance = abs(entry_price - stop_loss_price)  # Distance to stop loss in USD

    if stop_loss_distance == 0:
        raise ValueError("Stop loss distance must be greater than zero.")

    position_size = risk_amount / stop_loss_distance  # Position size in BTC
    return position_size
