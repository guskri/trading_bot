import pandas as pd

def load_data(file_path):
    """
    Load the data from a CSV file and prepare it.
    
    Args:
    - file_path (str): Path to the CSV file containing the trading data.
    
    Returns:
    - df (DataFrame): The prepared DataFrame with the trading data.
    """
    df = pd.read_csv(file_path)
    
    # Ensure the required columns are present
    required_columns = ['timestamp', 'close', 'high', 'low']
    for column in required_columns:
        if column not in df.columns:
            raise KeyError(f"Missing required column: {column}")

    # Ensure the timestamp column is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort data by timestamp
    df = df.sort_values('timestamp')
    
    return df
