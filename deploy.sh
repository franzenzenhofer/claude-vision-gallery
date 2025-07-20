#!/bin/bash
set -e

echo "🚀 Starting deployment process..."

# Run build script
echo "📦 Building with version number..."
node build.js

# Get version from version.json
VERSION=$(node -e "console.log(require('./version.json').version)")
echo "📌 Deploying version: $VERSION"

# Deploy to Cloudflare Pages
echo "☁️  Deploying to Cloudflare Pages..."
OUTPUT=$(wrangler pages deploy . --project-name=claude-vision 2>&1)
echo "$OUTPUT"

# Extract deployment URL
DEPLOY_URL=$(echo "$OUTPUT" | grep -oE 'https://[a-z0-9]+\.claude-vision\.pages\.dev' | head -1)

# Main URLs
MAIN_URL="https://claude-vision.pages.dev"

echo ""
echo "✅ Deployment Complete!"
echo "📦 Version: $VERSION"
echo "🌐 Main URL: $MAIN_URL"
echo "🔗 Deploy URL: $DEPLOY_URL"
echo ""
echo "🎨 Claude Vision Gallery v$VERSION is now live!"

# Output URLs for easy copying
echo ""
echo "URLs:"
echo "$MAIN_URL"
echo "$DEPLOY_URL"