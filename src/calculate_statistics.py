def calculate_statistics(trades_df):
    """
    Calculate strategy statistics like win rate, number of wins, losses, etc.
    
    Args:
    - trades_df (DataFrame): A DataFrame with the details of executed trades.
    
    Returns:
    - stats (dict): A dictionary containing various strategy statistics.
    """
    # Initialize counters
    wins = 0
    losses = 0
    current_streak = 0
    max_wins_in_a_row = 0
    max_losses_in_a_row = 0
    capital = []

    for i, row in trades_df.iterrows():
        if row['type'] in ['take_profit', 'sell', 'cover']:
            if row['capital'] > capital[-1]:
                wins += 1
                if current_streak >= 0:
                    current_streak += 1
                else:
                    current_streak = 1
                max_wins_in_a_row = max(max_wins_in_a_row, current_streak)
            else:
                losses += 1
                if current_streak <= 0:
                    current_streak -= 1
                else:
                    current_streak = -1
                max_losses_in_a_row = max(max_losses_in_a_row, -current_streak)
        capital.append(row['capital'])

    total_trades = wins + losses
    win_rate = wins / total_trades if total_trades > 0 else 0

    stats = {
        'Total Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Win Rate': win_rate,
        'Max Wins in a Row': max_wins_in_a_row,
        'Max Losses in a Row': max_losses_in_a_row
    }

    return stats

