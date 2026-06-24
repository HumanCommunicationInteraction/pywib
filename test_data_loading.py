#!/usr/bin/env python
"""Quick test script to verify data loading works correctly."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'test', 'balabit_dataset'))

from data_loader import load_all_sessions

# Test loading data
train_folder = 'test/balabit_dataset/train'
user_ids = [9, 12, 15, 16, 20, 21, 23, 29, 35]

print("Loading session data...")
df = load_all_sessions(train_folder, user_ids)

print(f"\nDataFrame shape: {df.shape}")
print(f"\nColumn names: {df.columns.tolist()}")
print(f"\nColumn data types:\n{df.dtypes}")
print(f"\nFirst few rows:\n{df.head()}")
print(f"\nEvent types present: {sorted(df['eventType'].unique())}")
print(f"\nNumber of sessions: {df['sessionId'].nunique()}")
print(f"\nSession IDs: {sorted(df['sessionId'].unique())[:10]}...")  # Show first 10

# Check if there are any NaN values
print(f"\nNull values:\n{df.isnull().sum()}")

# Save Df to CSV for inspection
output_csv = 'test_output.csv'
df.to_csv(output_csv, index=False)
print(f"\nDataFrame saved to {output_csv}")
