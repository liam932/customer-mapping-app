#!/usr/bin/env python3
"""
Filter Orders Script
Removes orders that have associated job_id since they're already in the app.
"""

import pandas as pd

def analyze_job_distribution(df):
    """Analyze the distribution of orders with/without job_id."""
    print("📊 Analyzing Job ID Distribution:")
    
    # Count orders with and without job_id
    has_job = df['job_id'].notna().sum()
    no_job = df['job_id'].isna().sum()
    total = len(df)
    
    print(f"  - Orders with job_id: {has_job} ({(has_job/total)*100:.1f}%)")
    print(f"  - Orders without job_id: {no_job} ({(no_job/total)*100:.1f}%)")
    print(f"  - Total orders: {total}")
    
    # Show revenue split
    revenue_with_job = df[df['job_id'].notna()]['total'].sum()
    revenue_without_job = df[df['job_id'].isna()]['total'].sum()
    total_revenue = df['total'].sum()
    
    print(f"\n💰 Revenue Distribution:")
    print(f"  - Revenue with job_id: ${revenue_with_job:,.2f} ({(revenue_with_job/total_revenue)*100:.1f}%)")
    print(f"  - Revenue without job_id: ${revenue_without_job:,.2f} ({(revenue_without_job/total_revenue)*100:.1f}%)")
    
    return has_job, no_job

def filter_orders(df):
    """Filter out orders that have job_id."""
    print("\n🔍 Filtering Orders:")
    
    # Keep only orders without job_id
    filtered_df = df[df['job_id'].isna()].copy()
    
    # Drop the job_id column since it's all NaN now
    filtered_df = filtered_df.drop(columns=['job_id'])
    
    print(f"  ✅ Removed {len(df) - len(filtered_df)} orders with job_id")
    print(f"  ✅ Kept {len(filtered_df)} orders without job_id")
    print(f"  ✅ Dropped job_id column (no longer needed)")
    
    return filtered_df

def main():
    """Main filtering function."""
    input_file = '/Users/liam/customer-mapping-app/cleaned_orders.csv'
    output_file = '/Users/liam/customer-mapping-app/orders_no_jobs.csv'
    
    print("🚀 Filtering Orders Without Job IDs")
    print("=" * 40)
    
    # Load cleaned data
    print("📂 Loading cleaned order data...")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df)} orders")
    
    # Analyze current distribution
    has_job, no_job = analyze_job_distribution(df)
    
    # Filter orders
    filtered_df = filter_orders(df)
    
    # Summary
    print(f"\n📋 Final Dataset Summary:")
    print(f"  - Columns: {list(filtered_df.columns)}")
    print(f"  - Rows: {len(filtered_df)}")
    
    # Revenue summary for filtered data
    total_revenue = filtered_df['total'].sum()
    avg_order = filtered_df['total'].mean()
    print(f"\n💰 Filtered Revenue Statistics:")
    print(f"  - Total Revenue: ${total_revenue:,.2f}")
    print(f"  - Average Order: ${avg_order:.2f}")
    print(f"  - Min Order: ${filtered_df['total'].min():.2f}")
    print(f"  - Max Order: ${filtered_df['total'].max():.2f}")
    
    # Date range for filtered data
    if 'completed_date' in filtered_df.columns:
        dates = pd.to_datetime(filtered_df['completed_date'], errors='coerce').dropna()
        if not dates.empty:
            print(f"\n📅 Date Range: {dates.min()} to {dates.max()}")
    
    # Status distribution
    if 'status' in filtered_df.columns:
        print(f"\n📈 Order Status Distribution:")
        status_counts = filtered_df['status'].value_counts()
        for status, count in status_counts.items():
            percentage = (count / len(filtered_df)) * 100
            print(f"  - {status}: {count} ({percentage:.1f}%)")
    
    # Save filtered data
    print(f"\n💾 Saving filtered data to: {output_file}")
    filtered_df.to_csv(output_file, index=False)
    print("  ✅ Filtered data saved successfully!")
    
    print(f"\n🎉 Filtering completed!")
    print(f"📁 Output file: {output_file}")
    print(f"📊 Removed {len(df) - len(filtered_df)} orders that had job_id")

if __name__ == "__main__":
    main()