import pandas as pd
from src.load_data import load_data
from src.calculate_indicators import calculate_macd_signals, find_swing_points
from src.simulate_trading import simulate_trading_strategy
from src.macd_bot import macd_strategy
from src.calculate_statistics import calculate_statistics

def main(file_path):
    """
    Main function to run the trading strategy simulation.
    
    Args:
    - file_path (str): Path to the CSV file containing the trading data.
    """
    # Load and prepare data
    df = load_data(file_path)
    print("Data loaded:")
    print(df.head())  # Debugging: Check data loaded

    # Calculate indicators
    df = calculate_macd_signals(df)
    print("\nIndicators calculated:")
    print(df[['timestamp', 'close', 'EMA12', 'EMA26', 'MACD', 'Signal_Line', 'EMA200']].head())  # Debugging: Check indicators

    # Identify swing highs and lows
    df = find_swing_points(df)
    print("\nSwing points identified:")
    print(df[['timestamp', 'Swing_High', 'Swing_Low']].dropna().head())  # Debugging: Check swing points

    # Generate trading signals
    df = macd_strategy(df)
    print("\nSignals generated:")
    print(df[['timestamp', 'Buy_Signal', 'Sell_Signal']].dropna().head())  # Debugging: Check signals

    # Simulate the trading strategy
    final_capital, trades_df = simulate_trading_strategy(df)
    print(f"\nFinal capital after trading: ${final_capital:.2f}")

    # Display the trades DataFrame
    if trades_df.empty:
        print("No trades were executed.")
    else:
        print("Executed trades:")
        print(trades_df)

        # Calculate and display strategy statistics
        stats = calculate_statistics(trades_df)
        print("\nStrategy Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    # Define the path to your CSV file
    file_path = './data/btc_usdt_5m_data.csv'

    # Run the main function
    main(file_path)
