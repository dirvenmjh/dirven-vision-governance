#!/usr/bin/env python3
"""Extract live symbols from working submission"""

import pandas as pd

# Read the working submission
df = pd.read_csv('C:\\NUMERAI_BEST3\\numerai_crypto_submission.csv')
symbols = df['symbol'].tolist()

print(f"Extracted {len(symbols)} symbols from live universe")

# Create Python list
code = "SYMBOLS_504 = [\n"
for i, sym in enumerate(symbols):
    if i % 10 == 0:
        code += "    "
    code += f"'{sym}', "
    if (i + 1) % 10 == 0:
        code += "\n"

# Remove trailing comma and newline
code = code.rstrip().rstrip(",") + ",\n]"

# Write to file
with open('symbols_504.py', 'w') as f:
    f.write('"""504 Numerai Crypto Live Universe symbols"""\n\n')
    f.write(code)
    f.write(f"\n# Total: {len(symbols)} symbols\n")
    f.write(f"assert len(SYMBOLS_504) == {len(symbols)}\n")

print("Updated symbols_504.py")
print(f"First 10: {symbols[:10]}")
print(f"Last 10: {symbols[-10:]}")
