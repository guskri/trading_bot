import numpy as np

def calculate_ema_signals(df, short_window=10, long_window=43):
    """
    Calculate the Exponential Moving Averages (EMAs) and generate trading signals.
    
    Args:
    - df (DataFrame): DataFrame containing the trading data.
    - short_window (int): The window size for the short-term EMA.
    - long_window (int): The window size for the long-term EMA.
    
    Returns:
    - df (DataFrame): DataFrame with added EMA and signal columns.
    """
    # Calculate EMAs
    df['EMA_short'] = df['close'].ewm(span=short_window, adjust=False).mean()
    df['EMA_long'] = df['close'].ewm(span=long_window, adjust=False).mean()

    # Generate signals: 1 for buy, -1 for sell, 0 for hold
    df['signal'] = np.where(df['EMA_short'] > df['EMA_long'], 1, 0)
    df['position'] = df['signal'].diff()  # Identify changes in signals

    return df
