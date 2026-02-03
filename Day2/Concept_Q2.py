import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import os
import sys
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def solve():
    # Read filename
    try:
        line = sys.stdin.readline()
        if not line:
            return
        filename = line.strip()
    except EOFError:
        return
        
    file_path = os.path.join(sys.path[0], filename)
    
    # Load dataset
    try:
        df = pd.read_csv(file_path)
    except Exception:
        return
    
    # Parse Datetime and set as index
    if 'Datetime' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df.set_index('Datetime', inplace=True)
    
    # Drop rows with missing values in Power_Consumption_diff
    df = df.dropna(subset=['Power_Consumption_diff'])
    
    # Set frequency (Monthly)
    if not df.index.freq:
        df.index.freq = pd.infer_freq(df.index)
    
    # Train-Test Split (80:20)
    train_size = int(len(df) * 0.8)
    test_size = len(df) - train_size
    
    train = df['Power_Consumption_diff'][:train_size]
    
    # Output sizes
    print(f"Training data size: {train_size}")
    print(f"Testing data size: {test_size}")
    
    # AR(2) Model
    ar_model = ARIMA(train, order=(2, 0, 0))
    ar_results = ar_model.fit()
    print("\nAR(2) Model Summary:")
    summary_ar = str(ar_results.summary())
    for line in summary_ar.split('\n'):
        print(line.rstrip())
    
    # MA(1) Model
    ma_model = ARIMA(train, order=(0, 0, 1))
    ma_results = ma_model.fit()
    print("\nMA(1) Model Summary:")
    summary_ma = str(ma_results.summary())
    for line in summary_ma.split('\n'):
        print(line.rstrip())

if __name__ == "__main__":
    solve()