"""
parse_reports.py - Convert wide-format supply usage reports to long format
"""

import pandas as pd
from datetime import datetime

# Configuration
INPUT_FILE = "data/raw/ReportJan_ICUs.txt"
OUTPUT_FILE = "data/processed/Long_To_Wide_MICU.csv"
TARGET_LOCATION = "UHMIC - UH MICU"
START_DATE = "01/01"
END_DATE = "01/22"


def parse_report_line(line):
    """Parse a single line from the report into structured data"""
    
    # Remove all quotes first
    line = line.replace('"', '')
    
    # Split by comma
    fields = [f.strip() for f in line.split(',')]
    
    try:
        # Helper function to find value after a descriptor
        def get_value_after(descriptor):
            """Find the value that comes after a descriptor field"""
            try:
                idx = fields.index(descriptor)
                # Return the next non-empty field
                for i in range(idx + 1, len(fields)):
                    if fields[i]:
                        return fields[i]
                return None
            except (ValueError, IndexError):
                return None
        
        # Extract metadata using descriptors
        facility = get_value_after("Facility:")
        location = get_value_after("Location:")
        active = get_value_after("Active:")
        min_qty = get_value_after("Min:")
        min_daily_usage = get_value_after("Min Daily Usage:")
        avg_usage = get_value_after("Avg Usage:")
        bin_loc = get_value_after("Bin:")
        critical = get_value_after("Critical:")
        max_qty = get_value_after("Max:")
        max_daily_usage = get_value_after("Max Daily Usage:")
        
        # Handle Item specially - it has both number and description
        item_idx = fields.index("Item:")
        item_no = fields[item_idx + 1] if item_idx + 1 < len(fields) else None
        item_desc = fields[item_idx + 2] if item_idx + 2 < len(fields) else None
        
        # Find where dates start (MM/DD pattern)
        date_start_idx = None
        for i, field in enumerate(fields):
            if '/' in field and len(field) == 5:  # Pattern like "01/01"
                date_start_idx = i
                break
        
        if date_start_idx is None:
            print(f"Warning: Could not find date start in line")
            return None
        
        # Extract dates (30 or 31 depending on month)
        dates = []
        values_start_idx = None
        
        for i in range(date_start_idx, len(fields)):
            if '/' in fields[i]:
                dates.append(fields[i])
            else:
                # Found first non-date field, this is where values start
                values_start_idx = i
                break
        
        # Extract values (same number as dates)
        values = fields[values_start_idx:values_start_idx + len(dates)]
        
        return {
            'facility': facility,
            'location': location,
            'item_no': item_no,
            'item_desc': item_desc,
            'active': active,
            'min_qty': min_qty,
            'min_daily_usage': min_daily_usage,
            'avg_usage': avg_usage,
            'bin_loc': bin_loc,
            'critical': critical,
            'max_qty': max_qty,
            'max_daily_usage': max_daily_usage,
            'dates': dates,
            'values': values
        }
    except (ValueError, IndexError) as e:
        print(f"Error parsing line: {e}")
        print(f"Fields found: {fields[:10]}...")  # Print first 10 fields for debugging
        return None


def convert_to_long_format(parsed_data):
    """Convert parsed data from wide to long format"""
    
    rows = []
    
    for data in parsed_data:
        if data is None:
            continue
            
        # Create a row for each date
        for date, value in zip(data['dates'], data['values']):
            # Filter by date range
            if START_DATE <= date <= END_DATE:
                row = {
                    'date': date,
                    'facility': data['facility'],
                    'location': data['location'],
                    'item_no': data['item_no'],
                    'item_desc': data['item_desc'],
                    'active': data['active'],
                    'min_qty': data['min_qty'],
                    'min_daily_usage': data['min_daily_usage'],
                    'avg_usage': data['avg_usage'],
                    'bin_loc': data['bin_loc'],
                    'critical': data['critical'],
                    'max_qty': data['max_qty'],
                    'max_daily_usage': data['max_daily_usage'],
                    'usage': value
                }
                rows.append(row)
    
    return rows


def main():
    """Main processing function"""
    
    print(f"Reading from: {INPUT_FILE}")
    print(f"Filtering for location: {TARGET_LOCATION}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print("\n" + "="*60)
    
    # Read and parse all lines
    parsed_data = []
    total_lines = 0
    successful_parses = 0
    
    with open(INPUT_FILE, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines only
            if not line:
                continue
            
            # Remove "END OF REPORT" from the end of the line if present
            if 'END OF REPORT' in line:
                line = line.replace('"END OF REPORT"', '').replace('END OF REPORT', '').rstrip(',').strip()
            
            total_lines += 1
            parsed = parse_report_line(line)
            
            # Debug: Print first parsed entry to see what we're getting
            if line_num == 1 and parsed:
                print("DEBUG - First parsed entry:")
                for key, val in parsed.items():
                    if key not in ['dates', 'values']:
                        print(f"  {key}: '{val}'")
                print(f"  Number of dates: {len(parsed['dates'])}")
                print(f"  Number of values: {len(parsed['values'])}")
                print("="*60 + "\n")
            
            if parsed:
                successful_parses += 1
                # Filter by location
                if parsed['location'] == TARGET_LOCATION:
                    parsed_data.append(parsed)
                elif line_num <= 3:  # Show first 3 mismatches
                    print(f"Location mismatch on line {line_num}:")
                    print(f"  Expected: '{TARGET_LOCATION}'")
                    print(f"  Found: '{parsed['location']}'")
            
            if line_num % 100 == 0:
                print(f"Processed {line_num} lines... ({successful_parses} parsed successfully)")
    
    print(f"\nTotal lines processed: {total_lines}")
    print(f"Successfully parsed: {successful_parses}")
    print(f"Matched location '{TARGET_LOCATION}': {len(parsed_data)}")
    
    if len(parsed_data) == 0:
        print("\n⚠️  WARNING: No entries matched the target location!")
        print("Check the debug output above to see what locations were found.")
        return
    
    # Convert to long format
    long_data = convert_to_long_format(parsed_data)
    
    print(f"Created {len(long_data)} long-format rows")
    
    # Create DataFrame and save
    df = pd.DataFrame(long_data)
    df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"\nOutput saved to: {OUTPUT_FILE}")
    print(f"\nFirst few rows:")
    print(df.head(10))
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nColumn names: {list(df.columns)}")


if __name__ == "__main__":
    main()