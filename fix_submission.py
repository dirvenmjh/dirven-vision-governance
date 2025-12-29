#!/usr/bin/env python3
"""Fix submission to only include valid Numerai symbols"""

import pandas as pd
import numpy as np
from symbols_504 import SYMBOLS_504

# Read current submission
df = pd.read_csv('numerai_submission_final.csv')

# Get list of valid symbols (real ones, not SYM*)
valid_symbols = [s for s in SYMBOLS_504 if not s.startswith('SYM')]

print(f"Total symbols in submission: {len(df)}")
print(f"Valid symbols: {len(valid_symbols)}")

# Filter to only valid symbols
df_valid = df[df['symbol'].isin(valid_symbols)].copy()

print(f"After filtering: {len(df_valid)} rows")

# Sort by symbol for consistency
df_valid = df_valid.sort_values('symbol').reset_index(drop=True)

# Ensure all signals are in valid range
df_valid['signal'] = np.clip(df_valid['signal'], 0.001, 0.999)

# Save
output_file = 'numerai_submission_final.csv'
df_valid.to_csv(output_file, index=False)

print(f"Saved {len(df_valid)} rows to {output_file}")
print(f"\nFirst 10:")
print(df_valid.head(10))
