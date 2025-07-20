#!/bin/bash
# Configure custom domain for Claude Vision Gallery

set -euo pipefail

PROJECT_NAME="claude-vision-gallery"
DOMAIN="claude-vision.franzai.com"
ZONE_ID="11bfe82c00e8c9e116e1e542b140f172"

echo "🌐 Configuring custom domain: $DOMAIN"

# Add custom domain to Cloudflare Pages project
echo "Adding domain to Pages project..."
curl -X POST \
  "https://api.cloudflare.com/client/v4/accounts/ecf21e85812dfa5b2a35245257fc71f5/pages/projects/$PROJECT_NAME/domains" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "'$DOMAIN'"
  }'

# Create CNAME record pointing to Pages
echo -e "\n\nCreating DNS record..."
curl -X POST \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "CNAME",
    "name": "claude-vision",
    "content": "'$PROJECT_NAME'.pages.dev",
    "ttl": 1,
    "proxied": true
  }'

echo -e "\n\n✅ Domain configuration complete!"
echo "🔗 Your gallery will be available at: https://$DOMAIN"
echo "⏱️  DNS propagation may take a few minutes."