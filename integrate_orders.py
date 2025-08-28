#!/usr/bin/env python3
"""
Integrate Orders into Customer Data
Adds orders data to the customer mapping JSON and creates the enhanced dataset.
"""

import json
import pandas as pd
from datetime import datetime

def load_data():
    """Load customer data and orders data."""
    print("📂 Loading data...")
    
    # Load customer data
    with open('/Users/liam/customer-mapping-app/customer_mapping_data.json', 'r') as f:
        customers = json.load(f)
    print(f"  ✅ Loaded {len(customers)} customers")
    
    # Load orders data
    orders_df = pd.read_csv('/Users/liam/customer-mapping-app/orders_no_jobs.csv')
    print(f"  ✅ Loaded {len(orders_df)} orders")
    
    return customers, orders_df

def integrate_orders(customers, orders_df):
    """Integrate orders data into customer records."""
    print("\n🔗 Integrating orders data...")
    
    # Convert orders to dictionary for faster lookup
    orders_by_org = {}
    for _, order in orders_df.iterrows():
        org_id = int(order['organisation_id']) if pd.notna(order['organisation_id']) else None
        if org_id:
            if org_id not in orders_by_org:
                orders_by_org[org_id] = []
            
            # Convert order to dictionary format
            order_dict = {
                'order_id': int(order['order_id']),
                'order_key': order['order_key'],
                'total': float(order['total']),
                'status': order['status'],
                'completed_date': order['completed_date'] if pd.notna(order['completed_date']) else None
            }
            orders_by_org[org_id].append(order_dict)
    
    print(f"  📊 Orders grouped by {len(orders_by_org)} organizations")
    
    # Add orders to customer records
    customers_with_orders = 0
    total_order_revenue = 0
    
    for customer in customers:
        customer_id = customer['id']
        if customer_id in orders_by_org:
            customer['orders'] = orders_by_org[customer_id]
            
            # Calculate order revenue
            order_revenue = sum(order['total'] for order in customer['orders'])
            customer['totalOrderRevenue'] = order_revenue
            total_order_revenue += order_revenue
            customers_with_orders += 1
            
            # Find latest order date
            valid_dates = [order['completed_date'] for order in customer['orders'] 
                          if order['completed_date'] and order['completed_date'] != 'NaN']
            if valid_dates:
                latest_order = max(valid_dates)
                customer['lastOrderDate'] = latest_order
            else:
                customer['lastOrderDate'] = None
        else:
            customer['orders'] = []
            customer['totalOrderRevenue'] = 0
            customer['lastOrderDate'] = None
    
    print(f"  ✅ Added orders to {customers_with_orders} customers")
    print(f"  💰 Total order revenue: ${total_order_revenue:,.2f}")
    
    return customers

def analyze_customer_segments(customers):
    """Analyze different customer segments."""
    print("\n📊 Analyzing Customer Segments:")
    
    # Count different segments
    has_jobs_only = 0
    has_orders_only = 0  
    has_both = 0
    has_neither = 0
    
    jobs_revenue = 0
    orders_revenue = 0
    
    for customer in customers:
        has_jobs = len(customer.get('jobs', [])) > 0
        has_orders = len(customer.get('orders', [])) > 0
        
        if has_jobs and has_orders:
            has_both += 1
        elif has_jobs and not has_orders:
            has_jobs_only += 1
        elif not has_jobs and has_orders:
            has_orders_only += 1
        else:
            has_neither += 1
        
        jobs_revenue += customer.get('totalRevenue', 0)
        orders_revenue += customer.get('totalOrderRevenue', 0)
    
    total = len(customers)
    print(f"  - Customers with jobs only: {has_jobs_only} ({(has_jobs_only/total)*100:.1f}%)")
    print(f"  - Customers with orders only: {has_orders_only} ({(has_orders_only/total)*100:.1f}%)")
    print(f"  - Customers with both jobs AND orders: {has_both} ({(has_both/total)*100:.1f}%)")
    print(f"  - Customers with neither: {has_neither} ({(has_neither/total)*100:.1f}%)")
    
    print(f"\n💰 Revenue Breakdown:")
    print(f"  - Total jobs revenue: ${jobs_revenue:,.2f}")
    print(f"  - Total orders revenue: ${orders_revenue:,.2f}")
    print(f"  - Combined revenue: ${(jobs_revenue + orders_revenue):,.2f}")
    
    return {
        'has_jobs_only': has_jobs_only,
        'has_orders_only': has_orders_only,
        'has_both': has_both,
        'has_neither': has_neither
    }

def save_enhanced_data(customers):
    """Save the enhanced customer data."""
    output_file = '/Users/liam/customer-mapping-app/customer_mapping_data_enhanced.json'
    
    print(f"\n💾 Saving enhanced data to: {output_file}")
    with open(output_file, 'w') as f:
        json.dump(customers, f, indent=2, default=str)
    
    print("  ✅ Enhanced data saved successfully!")
    return output_file

def main():
    """Main integration function."""
    print("🚀 Integrating Orders into Customer Data")
    print("=" * 45)
    
    # Load data
    customers, orders_df = load_data()
    
    # Integrate orders
    enhanced_customers = integrate_orders(customers, orders_df)
    
    # Analyze segments
    segments = analyze_customer_segments(enhanced_customers)
    
    # Save enhanced data
    output_file = save_enhanced_data(enhanced_customers)
    
    print(f"\n🎉 Integration completed!")
    print(f"📁 Enhanced dataset: {output_file}")
    print(f"🔍 Ready for jobs/orders toggle and filtering features!")

if __name__ == "__main__":
    main()