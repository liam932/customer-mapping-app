# Deployment Guide - Customer Mapping App

## Prerequisites

1. **Google Maps API Key** - Required for map functionality
2. **Node.js environment** - Version 16+ recommended
3. **Deployment platform** - Supports Node.js (Heroku, Railway, Vercel, etc.)

## Getting Your Google Maps API Key

### Step 1: Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable billing (required for Maps API)

### Step 2: Enable Required APIs
Enable these APIs in the Google Cloud Console:
- **Maps JavaScript API** - For displaying the interactive map
- **Geocoding API** - For address search functionality

### Step 3: Create API Key
1. Go to **APIs & Services > Credentials**
2. Click **+ CREATE CREDENTIALS > API Key**
3. Copy your API key

### Step 4: Secure Your API Key (IMPORTANT!)

#### Application Restrictions
Set **Application restrictions** to **HTTP referrers (web sites)**:
- For development: `http://localhost:3001/*`
- For production: `https://yourdomain.com/*`

#### API Restrictions
Restrict the key to only these APIs:
- Maps JavaScript API
- Geocoding API

## Environment Variables

### Development (.env file)
```bash
# Copy .env.example to .env and update values
GOOGLE_MAPS_API_KEY=your-actual-api-key-here
PORT=3001
NODE_ENV=development
```

### Production Deployment
Set these environment variables in your deployment platform:

| Variable | Value | Required |
|----------|--------|----------|
| `GOOGLE_MAPS_API_KEY` | Your Google Maps API key | Yes |
| `PORT` | Platform sets automatically | No |
| `NODE_ENV` | `production` | Recommended |

## Platform-Specific Deployment

### Railway
1. Connect your GitHub repository
2. Set environment variables in Railway dashboard
3. Deploy automatically on push

### Heroku
```bash
heroku create your-app-name
heroku config:set GOOGLE_MAPS_API_KEY=your-api-key
git push heroku main
```

### Vercel
1. Connect GitHub repository
2. Set environment variables in Vercel dashboard
3. Deploy automatically

### DigitalOcean App Platform
1. Create app from GitHub
2. Set environment variables in app settings
3. Deploy

## Security Best Practices

### API Key Security
- ✅ **DO**: Restrict API key to specific domains
- ✅ **DO**: Restrict API key to required APIs only  
- ✅ **DO**: Use environment variables
- ✅ **DO**: Monitor API usage in Google Cloud Console
- ❌ **DON'T**: Commit API keys to version control
- ❌ **DON'T**: Use unrestricted API keys
- ❌ **DON'T**: Share API keys publicly

### Application Security
- Set up HTTPS for production
- Consider rate limiting for API endpoints
- Monitor for unusual usage patterns

## Testing Your Deployment

1. **API Key Test**: Check `/api/config` endpoint returns the API key
2. **Map Loading**: Verify map loads without errors
3. **Address Search**: Test geocoding functionality
4. **Customer Data**: Ensure customer markers display correctly

## Troubleshooting

### Common Issues

**Map not loading:**
- Check API key is set correctly
- Verify Maps JavaScript API is enabled
- Check browser console for errors

**Address search not working:**
- Verify Geocoding API is enabled
- Check API key restrictions allow your domain

**API key errors:**
- Ensure API key has correct restrictions
- Verify billing is enabled in Google Cloud

### Cost Management

Monitor your Google Maps API usage:
1. Go to Google Cloud Console > APIs & Services > Dashboard
2. Set up billing alerts
3. Consider implementing client-side caching
4. Use API quotas to prevent unexpected charges

## Support

For Google Maps API issues:
- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [Google Maps Platform Support](https://developers.google.com/maps/support)

For deployment platform issues:
- Check your platform's specific documentation
- Contact platform support if needed