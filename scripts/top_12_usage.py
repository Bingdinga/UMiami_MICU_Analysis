"""
top_12_usage.py - Extract top 12 items by average daily usage
"""

import pandas as pd

# Configuration
INPUT_FILE = "data/processed/MICU_Data_Summary_Nurse_Req.csv"
OUTPUT_FILE = "data/processed/12_Highest_Usage.csv"


def main():
    """Extract top 12 items by avg_daily_usage"""
    
    print(f"Reading from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, keep_default_na=False, na_values=[''])
    
    print(f"Input shape: {df.shape}")
    
    # Sort by avg_daily_usage in descending order and take top 12
    df_top12 = df.nlargest(12, 'avg_daily_usage')
    
    print(f"\nTop 12 items by average daily usage:")
    print(df_top12[['item_no', 'item_desc', 'avg_daily_usage']])
    
    # Save to CSV
    df_top12.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    print(f"Output shape: {df_top12.shape}")


if __name__ == "__main__":
    main()