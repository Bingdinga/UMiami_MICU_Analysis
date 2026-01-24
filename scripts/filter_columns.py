"""
filter_columns.py - Extract and reorder specific columns from parsed data
"""

import pandas as pd

# Configuration
INPUT_FILE = "data/processed/Long_To_Wide_MICU.csv"
OUTPUT_FILE = "data/processed/MICU_Main_Data.csv"

# Columns to keep (in desired order)
COLUMNS_TO_KEEP = ['date', 'item_no', 'usage', 'item_desc', 'bin_loc']


def main():
    """Filter and reorder columns"""
    
    print(f"Reading from: {INPUT_FILE}")
    
    # Read the input CSV
    df = pd.read_csv(INPUT_FILE)
    
    print(f"Input shape: {df.shape}")
    print(f"Input columns: {list(df.columns)}")
    
    # Select and reorder columns
    df_filtered = df[COLUMNS_TO_KEEP]
    
    print(f"\nOutput shape: {df_filtered.shape}")
    print(f"Output columns: {list(df_filtered.columns)}")
    
    # Save to new CSV
    df_filtered.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    print(f"\nFirst few rows:")
    print(df_filtered.head(10))


if __name__ == "__main__":
    main()