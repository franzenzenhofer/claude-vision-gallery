#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Generate version from timestamp
const version = new Date().toISOString().replace(/[:\-]/g, '').split('.')[0]; // Format: 20250120T171234
const versionShort = version.slice(0, 8) + '.' + version.slice(9, 13); // Format: 20250120.1712

console.log('🚀 Building Claude Vision Gallery...');
console.log(`📦 Version: ${versionShort}`);

// Read and update index.html
let indexHtml = fs.readFileSync('index.html', 'utf8');

// Update CSS and JS references with new version
indexHtml = indexHtml.replace(/styles\.css\?v=[\d\.]+/g, `styles.css?v=${versionShort}`);
indexHtml = indexHtml.replace(/gallery\.js\?v=[\d\.]+/g, `gallery.js?v=${versionShort}`);

// Add version number to page (in footer or hidden meta)
if (!indexHtml.includes('data-version')) {
    indexHtml = indexHtml.replace(
        '<footer class="footer">',
        `<footer class="footer" data-version="${versionShort}">`
    );
}

// Write updated index.html
fs.writeFileSync('index.html', indexHtml);
console.log('✅ Updated index.html with version ' + versionShort);

// Read and update gallery.js to use consistent version
let galleryJs = fs.readFileSync('gallery.js', 'utf8');

// Replace the version line with new version
galleryJs = galleryJs.replace(
    /const version = .*?;/,
    `const version = '${versionShort}';`
);

// Write updated gallery.js
fs.writeFileSync('gallery.js', galleryJs);
console.log('✅ Updated gallery.js with version ' + versionShort);

// Create version.json for tracking
const versionInfo = {
    version: versionShort,
    buildTime: new Date().toISOString(),
    commit: process.env.GITHUB_SHA || 'local',
    images: 16
};

fs.writeFileSync('version.json', JSON.stringify(versionInfo, null, 2));
console.log('✅ Created version.json');

console.log('\n✨ Build complete!');
console.log(`📌 Version ${versionShort} ready to deploy`);
console.log('🌐 Deploy with: npm run deploy');