#!/bin/bash

echo "🔗 Setting up GitHub remote and pushing changes..."
echo ""
echo "⚠️  IMPORTANT: Replace 'YOURUSERNAME' with your actual GitHub username!"
echo ""

# Add GitHub remote (REPLACE YOURUSERNAME!)
git remote add origin https://github.com/YOURUSERNAME/customer-mapping-app.git

# Set main branch and push
git branch -M main
git push -u origin main

echo ""
echo "✅ Changes pushed to GitHub!"
echo "🚂 Railway should now auto-deploy with health check fixes!"