// Enhanced geocoding functions for accurate Australian address mapping

// Validate coordinates are within Australian bounds
function isValidAustralianCoordinate(lat, lng) {
    const AUSTRALIA_BOUNDS = {
        north: -10,
        south: -44,
        east: 154,
        west: 113
    };
    
    return lat >= AUSTRALIA_BOUNDS.south && lat <= AUSTRALIA_BOUNDS.north &&
           lng >= AUSTRALIA_BOUNDS.west && lng <= AUSTRALIA_BOUNDS.east;
}

// Geocode address using Google Maps Geocoding API
async function geocodeAddress(address, customer, geocoder) {
    return new Promise((resolve) => {
        const fullAddress = `${address}, Australia`;
        
        geocoder.geocode({ 
            address: fullAddress,
            region: 'AU',
            componentRestrictions: { country: 'AU' }
        }, (results, status) => {
            if (status === 'OK' && results && results.length > 0) {
                const location = results[0].geometry.location;
                const lat = location.lat();
                const lng = location.lng();
                
                if (isValidAustralianCoordinate(lat, lng)) {
                    console.log(`✅ Geocoded ${customer.name}: ${lat.toFixed(4)}, ${lng.toFixed(4)}`);
                    resolve({ lat, lng, geocoded: true });
                    return;
                }
            }
            
            console.warn(`❌ Geocoding failed for ${customer.name}: ${address}`);
            resolve(getFallbackCoordinates(customer));
        });
    });
}

// Get fallback coordinates based on city/state with better matching
function getFallbackCoordinates(customer) {
    const coordinates = {
        // Major Australian cities
        'Sydney': {lat: -33.8688, lng: 151.2093},
        'Melbourne': {lat: -37.8136, lng: 144.9631},
        'Brisbane': {lat: -27.4698, lng: 153.0251},
        'Perth': {lat: -31.9505, lng: 115.8605},
        'Adelaide': {lat: -34.9285, lng: 138.6007},
        'Canberra': {lat: -35.2809, lng: 149.1300},
        'Darwin': {lat: -12.4634, lng: 130.8456},
        'Hobart': {lat: -42.8821, lng: 147.3272},
        'Gold Coast': {lat: -28.0167, lng: 153.4000},
        'Cairns': {lat: -16.9203, lng: 145.7781},
        'Townsville': {lat: -19.2590, lng: 146.8169},
        'Geelong': {lat: -38.1499, lng: 144.3617},
        'Newcastle': {lat: -32.9283, lng: 151.7817},
        'Wollongong': {lat: -34.4278, lng: 150.8931},
        'Ballarat': {lat: -37.5622, lng: 143.8503},
        'Bendigo': {lat: -36.7570, lng: 144.2794},
        'Albury': {lat: -36.0737, lng: 146.9135},
        'Launceston': {lat: -41.4332, lng: 147.1441},
        'Mackay': {lat: -21.1559, lng: 149.1868},
        'Rockhampton': {lat: -23.3781, lng: 150.5132},
        
        // State/territory defaults
        'NSW': {lat: -33.8688, lng: 151.2093},
        'VIC': {lat: -37.8136, lng: 144.9631},
        'QLD': {lat: -27.4698, lng: 153.0251},
        'WA': {lat: -31.9505, lng: 115.8605},
        'SA': {lat: -34.9285, lng: 138.6007},
        'ACT': {lat: -35.2809, lng: 149.1300},
        'NT': {lat: -12.4634, lng: 130.8456},
        'TAS': {lat: -42.8821, lng: 147.3272}
    };
    
    const city = customer.location.city;
    const state = customer.location.state;
    
    // Try exact city match first (case insensitive)
    for (const [key, coords] of Object.entries(coordinates)) {
        if (city && city.toLowerCase() === key.toLowerCase()) {
            console.log(`📍 Fallback: ${customer.name} -> ${key}`);
            return { ...coords, geocoded: false };
        }
    }
    
    // Try partial city match
    for (const [key, coords] of Object.entries(coordinates)) {
        if (city && (
            city.toLowerCase().includes(key.toLowerCase()) ||
            key.toLowerCase().includes(city.toLowerCase())
        )) {
            console.log(`📍 Partial match: ${customer.name} -> ${key}`);
            return { ...coords, geocoded: false };
        }
    }
    
    // Fall back to state with random offset
    if (coordinates[state]) {
        const stateCoords = coordinates[state];
        const result = {
            lat: stateCoords.lat + (Math.random() - 0.5) * 0.5,
            lng: stateCoords.lng + (Math.random() - 0.5) * 0.5,
            geocoded: false
        };
        console.log(`📍 State fallback: ${customer.name} -> ${state}`);
        return result;
    }
    
    // Default to center of Australia
    console.warn(`❌ No coordinates found for ${customer.name} in ${city}, ${state}`);
    return {lat: -25.2744, lng: 133.7751, geocoded: false};
}

// Get coordinates for a customer with proper geocoding
async function getCustomerCoordinates(customer, geocoder, cache) {
    // If coordinates already exist and are valid, use them
    if (customer.location.lat && customer.location.lng && 
        isValidAustralianCoordinate(customer.location.lat, customer.location.lng)) {
        return { lat: customer.location.lat, lng: customer.location.lng, geocoded: true };
    }
    
    // Try geocoding the address
    if (customer.contact.address && customer.contact.address.trim()) {
        const address = customer.contact.address.trim();
        
        // Check cache first
        if (cache.has(address)) {
            return cache.get(address);
        }
        
        // Geocode the address
        const result = await geocodeAddress(address, customer, geocoder);
        cache.set(address, result);
        return result;
    }
    
    // Fall back to approximate coordinates
    return getFallbackCoordinates(customer);
}

// Export for use in HTML
window.geocodingUtils = {
    isValidAustralianCoordinate,
    geocodeAddress, 
    getFallbackCoordinates,
    getCustomerCoordinates
};