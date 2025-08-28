#!/usr/bin/env python3
"""
Order Data Cleaning Script
Cleans and standardizes order data from CSV export.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import re

def load_and_analyze_data(file_path):
    """Load CSV and analyze data quality issues."""
    print("📊 Loading order data...")
    
    # Load CSV with proper handling of BOM and encoding
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    print(f"✅ Loaded {len(df)} orders")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Basic info
    print("\n📈 Data Overview:")
    # Convert dates for analysis, handling mixed types
    dates = pd.to_datetime(df['Completed Date'], errors='coerce').dropna()
    if not dates.empty:
        print(f"  - Date range: {dates.min()} to {dates.max()}")
    else:
        print(f"  - Date range: No valid dates found")
    print(f"  - Total orders: {len(df)}")
    print(f"  - Order statuses: {df['Order Status'].value_counts().to_dict()}")
    
    return df

def identify_issues(df):
    """Identify data quality issues."""
    print("\n🔍 Identifying Data Issues:")
    issues = []
    
    # 1. BOM character in first column
    if df.columns[0].startswith('\ufeff'):
        issues.append("BOM character in header")
        print("  ❌ BOM character found in first column")
    
    # 2. Redundant columns
    redundant_cols = []
    if '_organisation_id' in df.columns and 'organisation_id' in df.columns:
        if (df['_organisation_id'] == 'field_61bc18e9eabb5').all():
            redundant_cols.append('_organisation_id')
    
    if '_job_id' in df.columns and 'job_id' in df.columns:
        if (df['_job_id'] == 'field_62202840d4d95').all() or df['_job_id'].isna().all():
            redundant_cols.append('_job_id')
    
    if redundant_cols:
        issues.append(f"Redundant columns: {redundant_cols}")
        print(f"  ❌ Redundant columns found: {redundant_cols}")
    
    # 3. Missing data
    missing_data = {}
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            missing_data[col] = missing_count
    
    if missing_data:
        issues.append("Missing data in columns")
        print("  ❌ Missing data:")
        for col, count in missing_data.items():
            percentage = (count / len(df)) * 100
            print(f"    - {col}: {count} ({percentage:.1f}%)")
    
    # 4. Date format issues
    if 'Completed Date' in df.columns:
        # Check for empty completion dates where status is completed
        incomplete_completed = df[(df['Order Status'] == 'wc-completed') & (df['Completed Date'].isna())]
        if not incomplete_completed.empty:
            issues.append(f"Completed orders without completion date: {len(incomplete_completed)}")
            print(f"  ❌ {len(incomplete_completed)} completed orders missing completion date")
    
    # 5. Order status issues
    if 'Order Status' in df.columns:
        statuses = df['Order Status'].unique()
        print(f"  ℹ️  Order statuses found: {list(statuses)}")
    
    # 6. Title redundancy
    if 'Title' in df.columns:
        # Check if title is just reformatted order date
        sample_titles = df['Title'].head(10).tolist()
        print(f"  ℹ️  Sample titles: {sample_titles[:3]}")
        if all("Order -" in str(title) for title in sample_titles if pd.notna(title)):
            issues.append("Title column contains redundant order date info")
            print("  ❌ Title column appears to be redundant (contains formatted order dates)")
    
    print(f"\n📋 Total issues found: {len(issues)}")
    return issues

def clean_data(df):
    """Clean and standardize the order data."""
    print("\n🧹 Cleaning Data:")
    cleaned_df = df.copy()
    
    # 1. Fix BOM character in column names
    cleaned_df.columns = [col.lstrip('\ufeff') for col in cleaned_df.columns]
    print("  ✅ Removed BOM character from headers")
    
    # 2. Remove redundant columns
    redundant_cols = []
    
    # Check _organisation_id - if it's always the same value, it's redundant
    if '_organisation_id' in cleaned_df.columns:
        unique_values = cleaned_df['_organisation_id'].unique()
        if len(unique_values) == 1 and unique_values[0] == 'field_61bc18e9eabb5':
            redundant_cols.append('_organisation_id')
    
    # Check _job_id - if it's always the same value or empty, it's redundant
    if '_job_id' in cleaned_df.columns:
        non_na_values = cleaned_df['_job_id'].dropna().unique()
        if len(non_na_values) <= 1 and (len(non_na_values) == 0 or non_na_values[0] == 'field_62202840d4d95'):
            redundant_cols.append('_job_id')
    
    if redundant_cols:
        cleaned_df = cleaned_df.drop(columns=redundant_cols)
        print(f"  ✅ Removed redundant columns: {redundant_cols}")
    
    # 3. Standardize column names
    column_mapping = {
        'Order ID': 'order_id',
        'Order Key': 'order_key', 
        'Title': 'title',
        'organisation_id': 'organisation_id',
        'Order Status': 'status',
        'Order Total': 'total',
        'Completed Date': 'completed_date',
        'job_id': 'job_id'
    }
    
    # Only rename columns that exist
    existing_mapping = {old: new for old, new in column_mapping.items() if old in cleaned_df.columns}
    cleaned_df = cleaned_df.rename(columns=existing_mapping)
    print(f"  ✅ Standardized column names: {list(existing_mapping.keys())}")
    
    # 4. Clean and standardize status values
    if 'status' in cleaned_df.columns:
        status_mapping = {
            'wc-completed': 'completed',
            'wc-pending': 'pending',
            'wc-processing': 'processing',
            'wc-on-hold': 'on_hold',
            'wc-cancelled': 'cancelled',
            'wc-refunded': 'refunded',
            'wc-failed': 'failed'
        }
        
        cleaned_df['status'] = cleaned_df['status'].map(status_mapping).fillna(cleaned_df['status'])
        print("  ✅ Standardized status values")
    
    # 5. Convert completed_date to proper datetime
    if 'completed_date' in cleaned_df.columns:
        cleaned_df['completed_date'] = pd.to_datetime(cleaned_df['completed_date'], errors='coerce')
        print("  ✅ Converted completion dates to datetime")
    
    # 6. Clean and convert total to numeric
    if 'total' in cleaned_df.columns:
        cleaned_df['total'] = pd.to_numeric(cleaned_df['total'], errors='coerce')
        print("  ✅ Converted order totals to numeric")
    
    # 7. Convert IDs to integers where possible
    id_columns = ['order_id', 'organisation_id', 'job_id']
    for col in id_columns:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').astype('Int64')
    print(f"  ✅ Converted ID columns to integers: {[c for c in id_columns if c in cleaned_df.columns]}")
    
    # 8. Remove title column if it's redundant
    if 'title' in cleaned_df.columns:
        # Check if all titles follow the pattern "Order - [date] @ [time]"
        sample_titles = cleaned_df['title'].dropna().head(20)
        if all("Order -" in str(title) for title in sample_titles):
            cleaned_df = cleaned_df.drop(columns=['title'])
            print("  ✅ Removed redundant title column")
    
    # 9. Sort by order_id
    if 'order_id' in cleaned_df.columns:
        cleaned_df = cleaned_df.sort_values('order_id').reset_index(drop=True)
        print("  ✅ Sorted by order ID")
    
    return cleaned_df

def generate_summary(original_df, cleaned_df):
    """Generate cleaning summary."""
    print("\n📊 Cleaning Summary:")
    print(f"  Original rows: {len(original_df)}")
    print(f"  Cleaned rows: {len(cleaned_df)}")
    print(f"  Original columns: {len(original_df.columns)}")
    print(f"  Cleaned columns: {len(cleaned_df.columns)}")
    
    print(f"\n📋 Final columns: {list(cleaned_df.columns)}")
    
    # Data quality stats
    if 'status' in cleaned_df.columns:
        print(f"\n📈 Order Status Distribution:")
        status_counts = cleaned_df['status'].value_counts()
        for status, count in status_counts.items():
            percentage = (count / len(cleaned_df)) * 100
            print(f"  - {status}: {count} ({percentage:.1f}%)")
    
    # Date range
    if 'completed_date' in cleaned_df.columns:
        min_date = cleaned_df['completed_date'].min()
        max_date = cleaned_df['completed_date'].max()
        print(f"\n📅 Date Range: {min_date} to {max_date}")
    
    # Revenue stats
    if 'total' in cleaned_df.columns:
        total_revenue = cleaned_df['total'].sum()
        avg_order = cleaned_df['total'].mean()
        print(f"\n💰 Revenue Statistics:")
        print(f"  - Total Revenue: ${total_revenue:,.2f}")
        print(f"  - Average Order: ${avg_order:.2f}")
        print(f"  - Min Order: ${cleaned_df['total'].min():.2f}")
        print(f"  - Max Order: ${cleaned_df['total'].max():.2f}")

def main():
    """Main cleaning function."""
    input_file = '/Users/liam/Downloads/Orders-for-app.csv'
    output_file = '/Users/liam/customer-mapping-app/cleaned_orders.csv'
    
    print("🚀 Starting Order Data Cleaning Process")
    print("=" * 50)
    
    # Load and analyze
    df = load_and_analyze_data(input_file)
    
    # Identify issues
    issues = identify_issues(df)
    
    # Clean data
    cleaned_df = clean_data(df)
    
    # Generate summary
    generate_summary(df, cleaned_df)
    
    # Save cleaned data
    print(f"\n💾 Saving cleaned data to: {output_file}")
    cleaned_df.to_csv(output_file, index=False)
    print("  ✅ Cleaned data saved successfully!")
    
    print("\n🎉 Data cleaning completed!")
    print(f"📁 Output file: {output_file}")

if __name__ == "__main__":
    main()