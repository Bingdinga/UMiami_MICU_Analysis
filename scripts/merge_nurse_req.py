"""
merge_nurse_req.py - Merge MICU data with nurse requisition data
"""

import pandas as pd
import numpy as np

# Configuration
MICU_DATA_FILE = "data/processed/MICU_Main_Data.csv"
NURSE_REQ_FILE = "data/raw/Nurse_Req_1_23_26.csv"
OUTPUT_FILE = "data/processed/MICU_Data_W_NurseReq.csv"


def main():
    """Merge MICU data with nurse requisition data"""
    
    print(f"Reading MICU data from: {MICU_DATA_FILE}")
    df_micu = pd.read_csv(MICU_DATA_FILE)
    
    print(f"Reading Nurse Req data from: {NURSE_REQ_FILE}")
    df_nurse = pd.read_csv(NURSE_REQ_FILE)
    
    print(f"\nMICU data shape: {df_micu.shape}")
    print(f"Nurse Req data shape: {df_nurse.shape}")
    
    # Rename Nurse Req columns to match our naming convention
    df_nurse = df_nurse.rename(columns={
        'Item Number': 'item_no',
        'Req. Min': 'req_min',
        'Req. Max': 'req_max',
        'Old Min': 'old_min',
        'Old Max': 'old_max'
    })
    
    # Convert item_no to string in both dataframes to ensure matching
    df_micu['item_no'] = df_micu['item_no'].astype(str)
    df_nurse['item_no'] = df_nurse['item_no'].astype(str)
    
    # Calculate average daily usage per item from MICU data
    avg_usage = df_micu.groupby('item_no')['usage'].mean().reset_index()
    avg_usage = avg_usage.rename(columns={'usage': 'avg_daily_usage'})
    avg_usage['avg_daily_usage'] = avg_usage['avg_daily_usage'].round(2)
    
    print(f"\nCalculated avg daily usage for {len(avg_usage)} items")
    
    # Find items in Nurse Req that are NOT in MICU data
    items_in_micu = set(df_micu['item_no'].unique())
    items_in_nurse = set(df_nurse['item_no'].unique())
    items_not_in_micu = items_in_nurse - items_in_micu
    
    print(f"\nItems in Nurse Req: {len(items_in_nurse)}")
    print(f"Items in MICU data: {len(items_in_micu)}")
    print(f"Items in Nurse Req but NOT in MICU: {len(items_not_in_micu)}")
    
    # Create placeholder rows for items not in MICU data
    placeholder_rows = []
    for item_no in items_not_in_micu:
        nurse_row = df_nurse[df_nurse['item_no'] == item_no].iloc[0]
        placeholder_rows.append({
            'date': '00/00',
            'item_no': item_no,
            'usage': 0,
            'item_desc': 'NOT IN MICU/RESEARCH ASAP',
            'bin_loc': 'NA',
            'avg_daily_usage': 0,
            'old_min': nurse_row['old_min'],
            'old_max': nurse_row['old_max'],
            'req_min': nurse_row['req_min'],
            'req_max': nurse_row['req_max']
        })
    
    df_placeholders = pd.DataFrame(placeholder_rows)
    
    # Merge MICU data with nurse req data (inner join to keep only shared items)
    df_merged = df_micu.merge(df_nurse, on='item_no', how='inner')
    
    # Add average daily usage to merged data
    df_merged = df_merged.merge(avg_usage, on='item_no', how='left')
    
    print(f"\nMerged data shape (before adding placeholders): {df_merged.shape}")
    
    # Combine merged data with placeholder rows
    if len(placeholder_rows) > 0:
        df_final = pd.concat([df_merged, df_placeholders], ignore_index=True)
    else:
        df_final = df_merged
    
    # Reorder columns to match desired output
    column_order = [
        'date', 'item_no', 'usage', 'item_desc', 'bin_loc',
        'avg_daily_usage', 'old_min', 'old_max', 'req_min', 'req_max'
    ]
    df_final = df_final[column_order]
    
    # Sort by item_no and date for readability
    df_final = df_final.sort_values(['item_no', 'date'])
    
    print(f"\nFinal data shape: {df_final.shape}")
    
    # Save to CSV
    df_final.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    print(f"\nFirst few rows:")
    print(df_final.head(15))
    
    # Show placeholder rows if any
    if len(placeholder_rows) > 0:
        print(f"\n\nPlaceholder rows for items not in MICU data:")
        print(df_final[df_final['date'] == '00/00'])
    
    print(f"\n\nColumn summary:")
    print(df_final.dtypes)


if __name__ == "__main__":
    main()