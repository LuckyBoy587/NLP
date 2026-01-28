import os
import sys

import pandas as pd

df = pd.read_csv(os.path.join(sys.path[0], input()))
print("First 5 rows of the dataset:")
print(df.head())

print("Missing values in dataset:")
print(df.drop(columns="Date").isna().sum())
print("Number of duplicate rows:", df.duplicated().sum())
print("Close price summary statistics:")
print(df["Close"].describe())