import os
import sys

def main():
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        return

    try:
        filename = input().strip()
        filepath = os.path.join(sys.path[0], filename)
        df = pd.read_csv(filepath)
    except Exception:
        return

    print("Dataset Preview:")
    print(df.head())

    print("\nDataset Information:")
    print(df.info())

    cols_to_check = ['Open', 'High', 'Low', 'Close', 'Volume', 'Close_diff']
    existing_cols = [c for c in cols_to_check if c in df.columns]
    
    print("\nMissing Value Check:")
    print(df[existing_cols].isnull().sum())
    
    df = df.dropna(subset=existing_cols)
    
    print("After missing value handling:")
    print(df[existing_cols].isnull().sum())

    train_size = int(len(df) * 0.8)
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]
    
    print("\nTrain-Test Split:")
    print(f"Training records: {len(train)}")
    print(f"Testing records: {len(test)}")

    print("\nSARIMA Model Summary:")
    try:
        import pmdarima as pm
        model = pm.auto_arima(train['Close'], 
                             seasonal=True, m=12,
                             suppress_warnings=True, 
                             error_action='ignore', 
                             stepwise=True)
        print(model.summary())
    except ImportError:
        print("pmdarima not available. SARIMA modeling skipped.")

if __name__ == "__main__":
    main()
