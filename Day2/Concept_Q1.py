import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import sys
import os

def solve():
    try:
        # Step 2: Load the dataset
        file_input = input().strip()
        filename = os.path.join(sys.path[0], file_input)
        
        if not os.path.exists(filename):
            print("File not found.")
            return
        
        df = pd.read_csv(filename)
        
        # Step 3: Parse date column
        df['DATE'] = pd.to_datetime(df['DATE'], dayfirst=True)
        df.set_index('DATE', inplace=True)
        
        # Output 1: First 5 rows of the dataset
        print("First 5 records of dataset:")
        print(df.head())
        print()
        
        # Step 5: Data preprocessing
        # Handle missing values using mean imputation
        df['Consumption'] = df['Consumption'].fillna(df['Consumption'].mean())
        
        # Handle outliers using IQR method
        Q1 = df['Consumption'].quantile(0.25)
        Q3 = df['Consumption'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df['Consumption'] = df['Consumption'].clip(lower=lower_bound, upper=upper_bound)
        
        # Output 2: Data preprocessing status
        print("Data preprocessing completed.")
        print()
        
        # Step 6: Additive decomposition
        add_result = seasonal_decompose(df['Consumption'], model='additive', period=12)
        
        # Output 3: Additive decomposition components
        print("Additive Model Components (First 5 Values)")
        print("Trend:")
        print(add_result.trend.dropna().head())
        print()
        print("Seasonality:")
        print(add_result.seasonal.head())
        print()
        print("Residuals:")
        print(add_result.resid.dropna().head())
        print()
        
        # Step 7: Multiplicative decomposition
        mul_result = seasonal_decompose(df['Consumption'], model='multiplicative', period=12)
        
        # Output 4: Multiplicative decomposition components
        print("Multiplicative Model Components (First 5 Values)")
        print("Trend:")
        print(mul_result.trend.dropna().head())
        print()
        print("Seasonality:")
        print(mul_result.seasonal.head())
        print()
        print("Residuals:")
        print(mul_result.resid.dropna().head())
        print()
        
        # Output 5: Model comparison conclusion
        print("Model Comparison Conclusion:")
        print("If seasonal values are constant → Additive model fits better.")
        print("If seasonal values change proportionally with trend → Multiplicative model fits better.")

    except Exception:
        pass

if __name__ == "__main__":
    solve()
