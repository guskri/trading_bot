def macd_strategy(df):

    # Generate buy and sell signals
    # Buy signal: MACD crosses below the center line (0) and Close is above EMA200
    df['Buy_Signal'] = ((df['MACD'].shift(1) > 0) & 
                        (df['MACD'] < 0) &
                        (df['close'] > df['EMA200']))

    # Sell signal: MACD crosses above the center line (0) and Close is below EMA200
    df['Sell_Signal'] = ((df['MACD'].shift(1) < 0) & 
                        (df['MACD'] > 0) &
                        (df['close'] < df['EMA200']))
                        
    return df