
# Risk Management Settings
INITIAL_CAPITAL = 10000       # Starting capital for trading
RISK_PER_TRADE = 0.01         # Risk per trade as a percentage of total capital (e.g., 0.02 for 2% risk)
RISK_REWARD_RATIO = 1.5       # Risk-reward ratio for trades (e.g., 2 for a 2:1 ratio)

# Strategy Settings
SHORT_EMA_WINDOW = 10         # Short-term EMA window for EMA strategy
LONG_EMA_WINDOW = 43          # Long-term EMA window for EMA strategy
MACD_SHORT_WINDOW = 12        # Short-term EMA window for MACD
MACD_LONG_WINDOW = 26         # Long-term EMA window for MACD
MACD_SIGNAL_WINDOW = 9        # Signal line EMA window for MACD
SWING_POINT_WINDOW = 9        # Window size for detecting swing highs/lows

# Trading Strategy Choice
DEFAULT_STRATEGY = 'MACD'     # Default strategy to use ('MACD' or 'EMA')
