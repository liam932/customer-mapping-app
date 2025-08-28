require('dotenv').config();
const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Load real customer data from JSON file
let allCustomers = [];
let customersWithJobs = [];
let customersWithoutJobs = [];
let customersWithOrders = [];
let customersWithBoth = [];

function loadCustomerData() {
  try {
    const dataPath = path.join(__dirname, 'customer_mapping_data_enhanced.json');
    const rawData = fs.readFileSync(dataPath, 'utf8');
    allCustomers = JSON.parse(rawData);
    
    // Add interaction recency calculation for each customer
    allCustomers = allCustomers.map(customer => {
      let latestInteractionDate = null;
      
      // Check last service date (already calculated at customer level)
      if (customer.lastServiceDate) {
        try {
          const serviceDate = new Date(customer.lastServiceDate);
          if (!isNaN(serviceDate.getTime())) {
            latestInteractionDate = serviceDate;
          }
        } catch (error) {
          console.warn(`Invalid lastServiceDate for ${customer.name}: ${customer.lastServiceDate}`);
        }
      }
      
      // Check last order date (already calculated at customer level)
      if (customer.lastOrderDate) {
        try {
          const orderDate = new Date(customer.lastOrderDate);
          if (!isNaN(orderDate.getTime())) {
            if (!latestInteractionDate || orderDate > latestInteractionDate) {
              latestInteractionDate = orderDate;
            }
          }
        } catch (error) {
          console.warn(`Invalid lastOrderDate for ${customer.name}: ${customer.lastOrderDate}`);
        }
      }
      
      // Add the calculated interaction date to customer
      customer.lastInteractionDate = latestInteractionDate ? latestInteractionDate.toISOString() : null;
      
      return customer;
    });
    
    // Split customers into different categories
    customersWithJobs = allCustomers.filter(customer => 
      customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0
    );
    
    customersWithoutJobs = allCustomers.filter(customer => 
      !customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0
    );
    
    // New categories for orders
    customersWithOrders = allCustomers.filter(customer => 
      customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0
    );
    
    customersWithBoth = allCustomers.filter(customer => 
      customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0 &&
      customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0
    );
    
    console.log(`Loaded enhanced customer data:`);
    console.log(`  - Total customers: ${allCustomers.length}`);
    console.log(`  - With jobs only: ${customersWithJobs.length - customersWithBoth.length}`);
    console.log(`  - With orders only: ${customersWithOrders.length - customersWithBoth.length}`);
    console.log(`  - With both jobs & orders: ${customersWithBoth.length}`);
    console.log(`  - With neither: ${allCustomers.length - customersWithJobs.length - (customersWithOrders.length - customersWithBoth.length)}`);
  } catch (error) {
    console.error('Error loading customer data:', error);
    allCustomers = [];
    customersWithJobs = [];
    customersWithoutJobs = [];
    customersWithOrders = [];
    customersWithBoth = [];
  }
}

// Load data on startup
loadCustomerData();

// API Routes
// Serve Google Maps API key
app.get('/api/config', (req, res) => {
  res.json({
    googleMapsApiKey: process.env.GOOGLE_MAPS_API_KEY || ''
  });
});

app.get('/api/customers', (req, res) => {
  const filterType = req.query.filterType || 'all';
  const showNonCustomers = req.query.showNonCustomers === 'true';
  
  let customers;
  
  switch (filterType) {
    case 'all':
      // Show all customers (only those with jobs or orders)
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
      break;
    case 'jobs_only':
      // Show customers who have jobs but no orders
      customers = allCustomers.filter(customer => 
        customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0 &&
        (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
      );
      break;
    case 'orders_only':
      // Show customers who have orders but no jobs
      customers = allCustomers.filter(customer => 
        customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0 &&
        (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0)
      );
      break;
    case 'both':
      // Show customers who have both jobs and orders
      customers = customersWithBoth;
      break;
    default:
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
  }
  
  // If showNonCustomers is true, also include organizations without jobs or orders
  if (showNonCustomers) {
    const nonCustomers = allCustomers.filter(customer => 
      (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0) &&
      (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
    );
    customers = customers.concat(nonCustomers);
  }
  
  res.json(customers);
});

app.get('/api/customers/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const customer = allCustomers.find(c => c.id === id);
  
  if (!customer) {
    return res.status(404).json({ error: 'Customer not found' });
  }
  
  res.json(customer);
});

// Get customers by organization type
app.get('/api/customers/type/:organizationType', (req, res) => {
  const organizationType = req.params.organizationType;
  const showWithoutJobs = req.query.showWithoutJobs === 'true';
  const customers = showWithoutJobs ? customersWithoutJobs : customersWithJobs;
  
  const filteredCustomers = customers.filter(c => 
    c.organizationType === organizationType
  );
  
  res.json(filteredCustomers);
});

// Get unique regions
app.get('/api/regions', (req, res) => {
  const filterType = req.query.filterType || 'all';
  const showNonCustomers = req.query.showNonCustomers === 'true';
  
  let customers;
  switch (filterType) {
    case 'all':
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
      break;
    case 'jobs_only':
      customers = allCustomers.filter(customer => 
        customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0 &&
        (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
      );
      break;
    case 'orders_only':
      customers = allCustomers.filter(customer => 
        customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0 &&
        (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0)
      );
      break;
    case 'both':
      customers = customersWithBoth;
      break;
    default:
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
  }
  
  if (showNonCustomers) {
    const nonCustomers = allCustomers.filter(customer => 
      (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0) &&
      (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
    );
    customers = customers.concat(nonCustomers);
  }
  
  const regions = [...new Set(customers.map(c => c.region).filter(r => r))].sort();
  res.json(regions);
});

// Get unique states with data cleaning and normalization
app.get('/api/states', (req, res) => {
  const filterType = req.query.filterType || 'all';
  const showNonCustomers = req.query.showNonCustomers === 'true';
  
  let customers;
  switch (filterType) {
    case 'all':
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
      break;
    case 'jobs_only':
      customers = allCustomers.filter(customer => 
        customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0 &&
        (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
      );
      break;
    case 'orders_only':
      customers = allCustomers.filter(customer => 
        customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0 &&
        (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0)
      );
      break;
    case 'both':
      customers = customersWithBoth;
      break;
    default:
      customers = allCustomers.filter(customer => 
        (customer.jobs && customer.jobs.length > 0 && customer.totalRevenue > 0) ||
        (customer.orders && customer.orders.length > 0 && customer.totalOrderRevenue > 0)
      );
  }
  
  if (showNonCustomers) {
    const nonCustomers = allCustomers.filter(customer => 
      (!customer.jobs || customer.jobs.length === 0 || customer.totalRevenue === 0) &&
      (!customer.orders || customer.orders.length === 0 || customer.totalOrderRevenue === 0)
    );
    customers = customers.concat(nonCustomers);
  }
  
  const stateMapping = {
    'NSW': 'NSW',
    'NSW ': 'NSW', 
    'nsw': 'NSW',
    'VIC': 'VIC',
    'Vic': 'VIC',
    'vic': 'VIC',
    'QLD': 'QLD',
    'QLD ': 'QLD',
    'SA': 'SA',
    'WA': 'WA',
    'ACT': 'ACT',
    'NT': 'NT',
    'TAS': 'TAS',
    'FNQ': 'QLD' // Far North Queensland -> QLD
  };
  
  const rawStates = customers.map(c => c.location.state).filter(s => s);
  const normalizedStates = rawStates
    .map(state => state.trim()) // Remove leading/trailing spaces
    .map(state => stateMapping[state] || state) // Normalize known variations
    .filter(state => state.length <= 3 && isNaN(state)) // Remove invalid values like postcodes
    .filter(state => ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'ACT', 'NT', 'TAS'].includes(state)); // Only valid Australian states
  
  const uniqueStates = [...new Set(normalizedStates)].sort();
  res.json(uniqueStates);
});

// Add new customer
app.post('/api/customers', (req, res) => {
  const newCustomer = {
    id: customers.length + 1,
    ...req.body
  };
  
  customers.push(newCustomer);
  res.status(201).json(newCustomer);
});

app.listen(PORT, () => {
  console.log(`Customer mapping server running on http://localhost:${PORT}`);
});