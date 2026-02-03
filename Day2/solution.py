import pandas as pd
import numpy as np
import os
import sys
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def solve():
    # Input format: CSV File Input
    try:
        # Use sys.stdin.read().strip() or input()?
        # The prompt says "The program prompts the user to enter the name of the CSV file"
        # So input() is correct.
        filename = input().strip()
        file_path = os.path.join(sys.path[0], filename)
        df = pd.read_csv(file_path)
    except Exception:
        return

    # Data Cleaning
    if 'Date' in df.columns:
        date_col = 'Date'
    elif 'Datetime' in df.columns:
        date_col = 'Datetime'
    else:
        # Fallback to identify date column if names differ slightly
        date_col = df.columns[0]

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    # Drop missing values in Close_diff
    df = df.dropna(subset=['Close_diff'])
    
    # Set Date as index
    df.set_index(date_col, inplace=True)
    
    # Train-Test Split (80% training, 20% testing)
    train_size = int(len(df) * 0.8)
    test_size = len(df) - train_size
    
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]
    
    print(f"Training data size: {train_size}")
    print(f"Testing data size: {test_size}")
    print()
    
    # Model Selection
    best_aic = np.inf
    best_order = None
    best_type = None
    
    results = {}
    
    # AR(p) models for p = 1 to 5
    for p in range(1, 6):
        try:
            model = ARIMA(train['Close_diff'], order=(p, 0, 0))
            res = model.fit()
            aic = res.aic
            results[f"AR({p})"] = aic
            if aic < best_aic:
                best_aic = aic
                best_order = p
                best_type = "AR"
        except:
            pass
            
    # MA(q) models for q = 1 to 5
    for q in range(1, 6):
        try:
            model = ARIMA(train['Close_diff'], order=(0, 0, q))
            res = model.fit()
            aic = res.aic
            results[f"MA({q})"] = aic
            if aic < best_aic:
                best_aic = aic
                best_order = q
                best_type = "MA"
        except:
            pass

    # Print AIC Values
    for p in range(1, 6):
        key = f"AR({p})"
        if key in results:
            print(f"{key} AIC: {results[key]}")
    for q in range(1, 6):
        key = f"MA({q})"
        if key in results:
            print(f"{key} AIC: {results[key]}")
            
    print()
    print(f"Best Model: {best_type}({best_order})")
    
    # Fit the best model
    if best_type == "AR":
        final_model = ARIMA(train['Close_diff'], order=(best_order, 0, 0))
    else:
        final_model = ARIMA(train['Close_diff'], order=(0, 0, best_order))
    
    final_res = final_model.fit()
    
    # Print Model Summary
    print(final_res.summary())
    print()
    
    # Ljung-Box Test Results
    print("Ljung-Box Test Results:")
    lb_results = acorr_ljungbox(final_res.resid, lags=[1], return_df=True)
    print(lb_results)

if __name__ == "__main__":
    solve()