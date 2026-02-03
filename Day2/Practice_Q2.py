import pandas as pd
import numpy as np
import os
import sys
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
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
    
    # Identify Date column
    date_col = 'Date' if 'Date' in df.columns else ('Datetime' if 'Datetime' in df.columns else df.columns[0])
    
    # Parse Date and set as index
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    
    # Drop rows with missing values in Close_diff
    df = df.dropna(subset=['Close_diff'])
    df.set_index(date_col, inplace=True)
    
    # Train-Test Split (80:20)
    train_size = int(len(df) * 0.8)
    test_size = len(df) - train_size
    
    train = df['Close_diff'][:train_size]
    
    # Output sizes
    print(f"Training data size: {train_size}")
    print(f"Testing data size: {test_size}")
    print()
    
    # Grid Search for best AR(p) and MA(q) (1 to 5)
    best_aic = np.inf
    best_order = None
    best_type = ""
    
    results_aic = {}
    
    # AR(p) models
    for p in range(1, 6):
        try:
            model = ARIMA(train, order=(p, 0, 0))
            res = model.fit()
            aic = res.aic
            print(f"AR({p}) AIC: {aic}")
            if aic < best_aic:
                best_aic = aic
                best_order = p
                best_type = "AR"
        except:
            pass
            
    # MA(q) models
    for q in range(1, 6):
        try:
            model = ARIMA(train, order=(0, 0, q))
            res = model.fit()
            aic = res.aic
            print(f"MA({q}) AIC: {aic}")
            if aic < best_aic:
                best_aic = aic
                best_order = q
                best_type = "MA"
        except:
            pass
            
    print()
    print(f"Best Model: {best_type}({best_order})")
    
    # Fit the best model
    if best_type == "AR":
        final_model = ARIMA(train, order=(best_order, 0, 0))
    else:
        final_model = ARIMA(train, order=(0, 0, best_order))
    
    final_res = final_model.fit()
    
    # Print Model Summary
    print(final_res.summary())
    print()
    
    # Ljung-Box Test Results at Lag 1
    print("Ljung-Box Test Results:")
    lb_results = acorr_ljungbox(final_res.resid, lags=[1], return_df=True)
    print(lb_results)

if __name__ == "__main__":
    solve()
