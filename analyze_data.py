#!/usr/bin/env python3
import json

# Load the customer data
with open('customer_mapping_data.json', 'r') as f:
    customers = json.load(f)

# Show distribution by organization type
org_types = {}
for customer in customers:
    org_type = customer['organizationType']
    if org_type not in org_types:
        org_types[org_type] = 0
    org_types[org_type] += 1

print('Organization Type Distribution:')
for org_type, count in sorted(org_types.items()):
    print(f'{org_type}: {count} customers')

print()

# Show some examples of each type
for org_type in ['school', 'university', 'industry']:
    examples = [c for c in customers if c['organizationType'] == org_type][:3]
    print(f'Sample {org_type} customers:')
    for customer in examples:
        print(f'  - {customer["name"]} (ID: {customer["id"]}, Revenue: ${customer["totalRevenue"]:.2f})')
    print()

# Show customers with highest revenue
top_customers = sorted(customers, key=lambda x: x['totalRevenue'], reverse=True)[:10]
print('Top 10 customers by revenue:')
for i, customer in enumerate(top_customers, 1):
    print(f'{i:2d}. {customer["name"]} - ${customer["totalRevenue"]:,.2f} ({customer["organizationType"]})')