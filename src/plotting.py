import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_price_and_capital(df, trades_df, initial_capital=10000):
    """
    Plot both the ticker price with buy/sell signals and the capital evolution on the same plot.
    
    Args:
    - df (DataFrame): DataFrame containing the trading data.
    - trades_df (DataFrame): DataFrame containing the executed trades.
    - initial_capital (float): Starting capital for the trading simulation.
    """
    if trades_df.empty:
        print("No trades were executed, nothing to plot.")
        return

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot close price
    ax1.plot(df['timestamp'], df['close'], label='Close Price', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Price (USD)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Plot buy and sell signals on price axis
    buy_signals = trades_df[trades_df['type'].str.contains('buy', case=False)]
    sell_signals = trades_df[trades_df['type'].str.contains('sell', case=False)]

    ax1.plot(buy_signals['timestamp'], buy_signals['price'], '^', markersize=10, color='green', lw=0, label='Buy Signal')
    ax1.plot(sell_signals['timestamp'], sell_signals['price'], 'v', markersize=10, color='red', lw=0, label='Sell Signal')

    ax1.legend(loc='upper left')

    # Create a second y-axis for the capital evolution plot
    ax2 = ax1.twinx()
    
    # Ensure the Capital column is initialized with the correct data type
    df['Capital'] = float(initial_capital)

    # Calculate cumulative returns based on trade executions
    for index, trade in trades_df.iterrows():
        df.loc[df['timestamp'] >= trade['timestamp'], 'Capital'] = float(trade['capital'])

    # Plot capital evolution
    ax2.plot(df['timestamp'], df['Capital'], label='Capital', color='orange')
    ax2.set_ylabel('Capital (USD)', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    ax2.legend(loc='upper right')

    # Format x-axis
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.title("Price and Capital Evolution")
    plt.show()
