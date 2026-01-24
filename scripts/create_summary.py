"""
create_summary.py - Generate summary statistics for MICU data
"""

import pandas as pd
import numpy as np
import math

# Configuration
INPUT_FILE = "data/processed/MICU_Data_W_NurseReq.csv"
OUTPUT_FILE = "data/processed/MICU_Data_Summary_Nurse_Req.csv"


def main():
    """Generate summary statistics by item"""
    
    print(f"Reading from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    df = pd.read_csv(INPUT_FILE, keep_default_na=False, na_values=[''])
    
    print(f"Input shape: {df.shape}")
    
    # Group by item_no and calculate statistics
    summary_data = []
    
    for item_no, group in df.groupby('item_no'):
        # Filter out placeholder rows (date='00/00') for statistical calculations
        real_data = group[group['date'] != '00/00']
        
        if len(real_data) > 0:
            # Calculate statistics from real data
            avg_daily_usage = real_data['usage'].mean()
            std_dev = real_data['usage'].std()
            max_usage = real_data['usage'].max()
            
            # Calculate z-score of max usage
            if std_dev > 0:
                max_z_score = (max_usage - avg_daily_usage) / std_dev
            else:
                max_z_score = 0
            
            # Round avg_daily_usage to 2 decimal places
            avg_daily_usage = round(avg_daily_usage, 2)
            
            # Round std_dev to 2 decimal places
            std_dev = round(std_dev, 2)
            
            # Round max_z_score to 2 decimal places
            max_z_score = round(max_z_score, 2)
        else:
            # Placeholder item with no real data
            avg_daily_usage = 0
            std_dev = 0
            max_z_score = 0
        
        # Calculate calc_min and calc_max (rounded up)
        calc_min = math.ceil(4 * avg_daily_usage)
        calc_max = math.ceil(8 * avg_daily_usage)
        
        # Get existing values (use first row since they're the same for all dates)
        first_row = group.iloc[0]
        
        summary_data.append({
            'item_no': item_no,
            'avg_daily_usage': avg_daily_usage,
            'std_dev': std_dev,
            'max_z_score': max_z_score,
            'calc_min': calc_min,
            'old_min': first_row['old_min'],
            'req_min': first_row['req_min'],
            'calc_max': calc_max,
            'old_max': first_row['old_max'],
            'req_max': first_row['req_max'],
            'item_desc': first_row['item_desc'],
            'bin_loc': first_row['bin_loc']
        })
    
    # Create summary DataFrame
    df_summary = pd.DataFrame(summary_data)
    
    # Ensure column order
    column_order = [
        'item_no', 'avg_daily_usage', 'std_dev', 'max_z_score',
        'calc_min', 'old_min', 'req_min',
        'calc_max', 'old_max', 'req_max',
        'item_desc', 'bin_loc'
    ]
    df_summary = df_summary[column_order]
    
    # Sort by item_no
    df_summary = df_summary.sort_values('item_no')
    
    print(f"\nSummary shape: {df_summary.shape}")
    
    # Save to CSV
    df_summary.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    print(f"\nFirst few rows:")
    print(df_summary.head(10))
    
    print(f"\n\nSummary statistics:")
    print(f"Total items: {len(df_summary)}")
    print(f"Items with placeholder data (00/00): {len(df_summary[df_summary['avg_daily_usage'] == 0])}")
    print(f"\nColumn data types:")
    print(df_summary.dtypes)


if __name__ == "__main__":
    main()