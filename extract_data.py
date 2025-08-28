#!/usr/bin/env python3
import re
import json
import requests
import time
from datetime import datetime, timedelta

def parse_sql_value(value):
    """Parse a SQL value, removing quotes and handling NULL"""
    if value == 'NULL' or value == '':
        return None
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('""', '"')
    return value

def extract_organizations():
    """Extract organization data from SQL file"""
    with open('data/wp_mops_organisations.sql', 'r') as f:
        content = f.read()
    
    # Find all INSERT statements
    insert_pattern = r'INSERT INTO `wp_mops_organisations`[^V]*VALUES\s*(.*?)(?=INSERT|$)'
    insert_matches = re.findall(insert_pattern, content, re.DOTALL)
    
    organizations = []
    
    for insert_values in insert_matches:
        # Find individual value rows
        row_pattern = r'\(([^)]+)\)'
        rows = re.findall(row_pattern, insert_values, re.DOTALL)
        
        for row_data in rows:
            # Split by comma, respecting quoted strings
            values = []
            current_value = ''
            in_quotes = False
            quote_char = None
            
            i = 0
            while i < len(row_data):
                char = row_data[i]
                
                if not in_quotes and char in ["'", '"']:
                    in_quotes = True
                    quote_char = char
                    current_value += char
                elif in_quotes and char == quote_char:
                    # Check for escaped quote
                    if i + 1 < len(row_data) and row_data[i + 1] == quote_char:
                        current_value += char + char
                        i += 1
                    else:
                        in_quotes = False
                        quote_char = None
                        current_value += char
                elif not in_quotes and char == ',':
                    values.append(current_value.strip())
                    current_value = ''
                else:
                    current_value += char
                
                i += 1
            
            # Add the last value
            if current_value.strip():
                values.append(current_value.strip())
            
            # Extract organization data if we have enough values
            if len(values) >= 10:
                try:
                    org = {
                        'id': int(values[0]),
                        'region_id': int(values[1]) if values[1] != 'NULL' else None,
                        'organisation_type_id': int(values[2]) if values[2] != 'NULL' else None,
                        'title': parse_sql_value(values[3]) or '',
                        'physical_address_street': parse_sql_value(values[4]) or '',
                        'physical_address_suburb': parse_sql_value(values[5]) or '',
                        'physical_address_state': parse_sql_value(values[6]) or '',
                        'physical_address_postcode': parse_sql_value(values[7]) or '',
                        'email': parse_sql_value(values[8]) or '',
                        'phone': parse_sql_value(values[9]) or ''
                    }
                    organizations.append(org)
                except (ValueError, IndexError):
                    continue
    
    return organizations

def extract_regions():
    """Extract regions mapping"""
    with open('data/wp_mops_regions.sql', 'r') as f:
        content = f.read()
    
    regions_pattern = r'INSERT INTO `wp_mops_regions`.*?VALUES\s*(.*?);'
    regions_match = re.search(regions_pattern, content, re.DOTALL)
    
    regions_map = {}
    if regions_match:
        values_section = regions_match.group(1)
        row_pattern = r'\((\d+),\s*\'([^\']+)\',\s*\'[^\']*\'\)'
        regions_rows = re.findall(row_pattern, values_section)
        
        for region_id, region_name in regions_rows:
            regions_map[int(region_id)] = region_name
    
    return regions_map

def extract_organization_types():
    """Extract organization types mapping"""
    with open('data/wp_mops_organisation_types.sql', 'r') as f:
        content = f.read()
    
    types_pattern = r'INSERT INTO `wp_mops_organisation_types`.*?VALUES\s*(.*?);'
    types_match = re.search(types_pattern, content, re.DOTALL)
    
    org_types_map = {}
    if types_match:
        values_section = types_match.group(1)
        row_pattern = r'\((\d+),\s*\'([^\']+)\',\s*\'[^\']*\'\)'
        types_rows = re.findall(row_pattern, values_section)
        
        for type_id, type_name in types_rows:
            if type_name in ['School - Catholic', 'School - Government', 'School - Private']:
                org_types_map[int(type_id)] = 'school'
            elif type_name == 'University':
                org_types_map[int(type_id)] = 'university'
            elif type_name in ['Industry', 'Supplier']:
                org_types_map[int(type_id)] = 'industry'
            else:
                org_types_map[int(type_id)] = 'other'
    
    return org_types_map

def parse_datetime(datetime_str):
    """Parse datetime string and convert to AEST (+10 hours)"""
    if not datetime_str or datetime_str == 'NULL':
        return None
    
    try:
        # Remove quotes
        datetime_str = datetime_str.strip("'\"")
        # Parse the datetime
        dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        # Add 10 hours for AEST
        dt_aest = dt + timedelta(hours=10)
        return dt_aest.isoformat() + '+10:00'
    except (ValueError, TypeError):
        return None

def extract_jobs():
    """Extract jobs data from SQL file"""
    with open('data/wp_mops_jobs.sql', 'r') as f:
        lines = f.readlines()
    
    jobs = []
    
    # Parse line by line looking for job data rows
    for line in lines:
        line = line.strip()
        
        # Skip non-data lines
        if not line.startswith('(') or not line.endswith('),') and not line.endswith(');'):
            continue
            
        # Remove parentheses and trailing comma/semicolon
        if line.endswith('),'):
            row_data = line[1:-2]
        elif line.endswith(');'):
            row_data = line[1:-2]
        else:
            continue
            
        # Split by comma, respecting quoted strings
        values = []
        current_value = ''
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(row_data):
            char = row_data[i]
            
            if not in_quotes and char in ["'", '"']:
                in_quotes = True
                quote_char = char
                current_value += char
            elif in_quotes and char == quote_char:
                # Check for escaped quote
                if i + 1 < len(row_data) and row_data[i + 1] == quote_char:
                    current_value += char + char
                    i += 1
                else:
                    in_quotes = False
                    quote_char = None
                    current_value += char
            elif not in_quotes and char == ',':
                values.append(current_value.strip())
                current_value = ''
            else:
                current_value += char
            
            i += 1
        
        # Add the last value
        if current_value.strip():
            values.append(current_value.strip())
        
        # Extract job data if we have enough values (should be 21 for wp_mops_jobs)
        if len(values) >= 15:
            try:
                total_val = parse_sql_value(values[11])
                units_val = parse_sql_value(values[2])
                
                job = {
                    'id': int(values[0]),
                    'organisation_id': int(values[1]),
                    'total': float(total_val) if total_val else 0.0,
                    'units': int(units_val) if units_val else 0,
                    'status': parse_sql_value(values[14]) or '',
                    'completedDate': parse_datetime(parse_sql_value(values[13]))
                }
                jobs.append(job)
            except (ValueError, IndexError, TypeError) as e:
                continue
    
    return jobs

def geocode_address_nominatim(address):
    """Geocode address using OpenStreetMap Nominatim (free service)"""
    if not address or not address.strip():
        return None, None
    
    # Clean address for Australian geocoding
    clean_address = address.strip()
    if not 'Australia' in clean_address:
        clean_address += ', Australia'
    
    try:
        # Use Nominatim API (free, but with rate limiting)
        url = 'https://nominatim.openstreetmap.org/search'
        params = {
            'q': clean_address,
            'format': 'json',
            'countrycodes': 'AU',  # Restrict to Australia
            'limit': 1,
            'addressdetails': 1
        }
        
        headers = {
            'User-Agent': 'CustomerMappingApp/1.0 (contact@example.com)'  # Required by Nominatim
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            if results and len(results) > 0:
                result = results[0]
                lat = float(result['lat'])
                lng = float(result['lon'])
                
                # Validate coordinates are within Australia
                if -44 <= lat <= -10 and 113 <= lng <= 154:
                    print(f"✅ Geocoded: {address} -> {lat:.4f}, {lng:.4f}")
                    return lat, lng
                else:
                    print(f"❌ Invalid coordinates for {address}: {lat}, {lng}")
        
        print(f"❌ Geocoding failed for: {address}")
        return None, None
        
    except Exception as e:
        print(f"❌ Geocoding error for {address}: {str(e)}")
        return None, None

def postcode_to_state(postcode):
    """Convert Australian postcode to state"""
    if not postcode or not isinstance(postcode, str):
        return None
    
    # Clean the postcode - extract only digits
    clean_postcode = ''.join(filter(str.isdigit, str(postcode)))
    if not clean_postcode:
        return None
    
    try:
        pc = int(clean_postcode)
    except ValueError:
        return None
    
    # Australian postcode to state mapping
    if 1000 <= pc <= 2599 or 2619 <= pc <= 2898 or 2921 <= pc <= 2999:
        return 'NSW'
    elif 200 <= pc <= 299 or 2600 <= pc <= 2618 or 2900 <= pc <= 2920:
        return 'ACT'
    elif 3000 <= pc <= 3999 or 8000 <= pc <= 8999:
        return 'VIC'
    elif 4000 <= pc <= 4999 or 9000 <= pc <= 9999:
        return 'QLD'
    elif 5000 <= pc <= 5999:
        return 'SA'
    elif 6000 <= pc <= 6797 or 6800 <= pc <= 6999:
        return 'WA'
    elif 7000 <= pc <= 7999:
        return 'TAS'
    elif 800 <= pc <= 899 or 900 <= pc <= 999:
        return 'NT'
    else:
        return None

def build_customer_mapping_data():
    """Build the complete customer mapping JSON structure"""
    # Extract all data
    organizations = extract_organizations()
    regions = extract_regions()
    org_types = extract_organization_types()
    jobs = extract_jobs()
    
    # Group jobs by organization
    jobs_by_org = {}
    for job in jobs:
        org_id = job['organisation_id']
        if org_id not in jobs_by_org:
            jobs_by_org[org_id] = []
        jobs_by_org[org_id].append(job)
    
    # Build customer data
    customers = []
    states_fixed_count = 0
    geocoded_count = 0
    
    for org in organizations:
        org_id = org['id']
        org_jobs = jobs_by_org.get(org_id, [])
        
        # Calculate total revenue
        total_revenue = sum(job['total'] for job in org_jobs)
        
        # Find last service date
        last_service_date = None
        completed_dates = [job['completedDate'] for job in org_jobs if job['completedDate']]
        if completed_dates:
            # Convert ISO dates back to date strings for comparison
            dates_only = []
            for date_str in completed_dates:
                try:
                    # Extract just the date part from ISO format
                    date_part = date_str.split('T')[0]
                    dates_only.append(date_part)
                except:
                    continue
            if dates_only:
                last_service_date = max(dates_only)
        
        # Build address string
        address_parts = []
        if org['physical_address_street']:
            address_parts.append(org['physical_address_street'])
        if org['physical_address_suburb']:
            address_parts.append(org['physical_address_suburb'])
        if org['physical_address_state']:
            address_parts.append(org['physical_address_state'])
        if org['physical_address_postcode']:
            address_parts.append(org['physical_address_postcode'])
        
        full_address = ', '.join(address_parts) if address_parts else ''
        
        # Get region name
        region_name = regions.get(org['region_id'], '') if org['region_id'] else ''
        
        # Get organization type
        org_type = org_types.get(org['organisation_type_id'], 'other') if org['organisation_type_id'] else 'other'
        
        # Build jobs array
        job_list = []
        for job in org_jobs:
            job_data = {
                'total': job['total'],
                'units': job['units'],
                'status': job['status'],
                'completedDate': job['completedDate']
            }
            job_list.append(job_data)
        
        # Determine state - use original state or derive from postcode if missing
        original_state = org['physical_address_state']
        postcode = org['physical_address_postcode']
        
        # Clean and validate the original state
        clean_state = None
        if original_state:
            state_mapping = {
                'NSW': 'NSW', 'NSW ': 'NSW', 'nsw': 'NSW',
                'VIC': 'VIC', 'Vic': 'VIC', 'vic': 'VIC',
                'QLD': 'QLD', 'QLD ': 'QLD',
                'SA': 'SA', 'WA': 'WA', 'ACT': 'ACT', 'NT': 'NT', 'TAS': 'TAS',
                'FNQ': 'QLD'
            }
            trimmed = original_state.strip()
            normalized = state_mapping.get(trimmed, trimmed)
            valid_states = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'ACT', 'NT', 'TAS']
            if normalized in valid_states:
                clean_state = normalized
        
        # If no valid state, try to derive from postcode
        final_state = clean_state
        if not clean_state:
            final_state = postcode_to_state(postcode)
            if final_state:
                states_fixed_count += 1

        # Geocode ALL customers (both with and without jobs)
        lat, lng = None, None
        if full_address and full_address.strip():
            job_info = f"({len(org_jobs)} jobs)" if org_jobs else "(no jobs)"
            print(f"Geocoding {org['title']} {job_info}...")
            # Rate limiting: pause between geocoding requests
            time.sleep(1)  # 1 second delay to respect API limits
            lat, lng = geocode_address_nominatim(full_address)
            if lat and lng:
                geocoded_count += 1

        # Build customer object with geocoded coordinates
        customer = {
            'id': org_id,
            'name': org['title'],
            'contact': {
                'email': org['email'],
                'phone': org['phone'],
                'address': full_address
            },
            'location': {
                'lat': lat,
                'lng': lng,
                'city': org['physical_address_suburb'],
                'state': final_state,
                'postcode': org['physical_address_postcode']
            },
            'organizationType': org_type,
            'region': region_name,
            'jobs': job_list,
            'totalRevenue': total_revenue,
            'lastServiceDate': last_service_date
        }
        
        customers.append(customer)
    
    print(f"Fixed {states_fixed_count} customer states using postcode mapping")
    print(f"Geocoded {geocoded_count} addresses with coordinates")
    return customers

# Test the functions
if __name__ == "__main__":
    print("Building customer mapping data...")
    customers = build_customer_mapping_data()
    
    print(f"Built {len(customers)} customer records")
    
    # Show some statistics
    customers_with_jobs = [c for c in customers if c['jobs']]
    total_revenue_all = sum(c['totalRevenue'] for c in customers)
    
    print(f"Customers with jobs: {len(customers_with_jobs)}")
    print(f"Total revenue across all customers: ${total_revenue_all:,.2f}")
    
    # Show sample customers
    print("\nSample customers:")
    for customer in customers[:5]:
        print(f"ID: {customer['id']}")
        print(f"  Name: {customer['name']}")
        print(f"  Type: {customer['organizationType']}")
        print(f"  Region: {customer['region']}")
        print(f"  Jobs: {len(customer['jobs'])}")
        print(f"  Total Revenue: ${customer['totalRevenue']:,.2f}")
        print(f"  Last Service: {customer['lastServiceDate']}")
        print()
    
    # Save to JSON file
    with open('customer_mapping_data.json', 'w') as f:
        json.dump(customers, f, indent=2, ensure_ascii=False)
    
    print(f"Customer mapping data saved to customer_mapping_data.json")