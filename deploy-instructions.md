# 🚀 Deployment Instructions

## Step 1: Push to GitHub

After creating your GitHub repository, run these commands:

```bash
# Add GitHub remote (replace 'yourusername' with your actual GitHub username)
git remote add origin https://github.com/yourusername/customer-mapping-app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `customer-mapping-app` repository
4. Railway will automatically detect it's a Node.js app and start building

## Step 3: Add Environment Variables

In Railway dashboard:
1. Go to your project → Variables tab
2. Add this variable:
   - **GOOGLE_MAPS_API_KEY**: `your-actual-google-maps-api-key-here`

## Step 4: Get Your Google Maps API Key

If you don't have one yet:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable billing
3. Enable "Maps JavaScript API" and "Geocoding API"
4. Create credentials → API Key
5. **IMPORTANT**: Restrict the API key:
   - Application restrictions: HTTP referrers
   - Add your Railway domain: `https://*.railway.app/*`
   - API restrictions: Only Maps JavaScript API and Geocoding API

## Step 5: Test Your Live Application

Once deployed, Railway will give you a URL like:
`https://customer-mapping-app-production-xxxx.railway.app`

Test these features:
- ✅ Map loads correctly
- ✅ Customer markers appear
- ✅ Filtering works (All Data, Jobs Only, etc.)
- ✅ Toggle for non-customers works
- ✅ Address search functions
- ✅ Legend displays correctly

## Troubleshooting

**If map doesn't load:**
- Check Railway logs for errors
- Verify GOOGLE_MAPS_API_KEY is set
- Ensure API key restrictions include your Railway domain

**If data doesn't appear:**
- Check Railway logs for JSON loading errors
- Verify all data files were committed to GitHub

**If anything else breaks:**
- Check Railway logs in the dashboard
- Look for JavaScript errors in browser console