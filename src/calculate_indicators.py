    
def calculate_macd_signals(df):
    # Calculate the 12-period EMA
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()

    # Calculate the 26-period EMA
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()

    # Calculate MACD (the difference between 12-period EMA and 26-period EMA)
    df['MACD'] = df['EMA12'] - df['EMA26']

    # Calculate the 9-period EMA of MACD (Signal Line)
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Calculate the 200-period EMA
    df['EMA200'] = df['close'].ewm(span=200, adjust=False).mean()

    return df

def find_swing_points(df, window=5):

    df['Swing_High'] = df['high'].rolling(window=window, center=True).apply(lambda x: x.max() if x[window//2] == x.max() else float('nan'), raw=True)
    df['Swing_Low'] = df['low'].rolling(window=window, center=True).apply(lambda x: x.min() if x[window//2] == x.min() else float('nan'), raw=True)
    
    return df
