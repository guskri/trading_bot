from src.load_data import load_data
from src.calculate_indicators import calculate_macd_signals, find_swing_points
from src.simulate_trading import simulate_trading_strategy
from src.macd_bot import macd_strategy
from src.calculate_statistics import calculate_statistics
from src.plotting import plot_price_and_capital
from src.config import INITIAL_CAPITAL

def main(file_path):
    """
    Main function to run the trading strategy simulation.
    
    Args:
    - file_path (str): Path to the CSV file containing the trading data.
    """
    # Load and prepare data
    df = load_data(file_path)

    # Calculate indicators
    df = calculate_macd_signals(df)

    # Identify swing highs and lows
    df = find_swing_points(df)

    # Apply the MACD strategy to generate buy and sell signals
    print("running macd strat")
    df = macd_strategy(df)

    # Simulate the trading strategy
    final_capital, trades_df = simulate_trading_strategy(df)
    print(f"\nFinal capital after trading: ${final_capital:.2f}")

    # Print trades_df columns to check for 'type' column
    print("\nTrades DataFrame Columns:", trades_df.columns.tolist())  # Debugging line

    # Plot price and capital on the same plot
    plot_price_and_capital(df, trades_df, initial_capital=INITIAL_CAPITAL)

    # Calculate and display strategy statistics
    stats = calculate_statistics(trades_df)
    print("\nStrategy Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    # Define the path to your CSV file
    file_path = './data/eth_usdt_5m_data.csv'

    # Run the main function
    main(file_path)
