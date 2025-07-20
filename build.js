#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Get current timestamp for cache busting
const version = Date.now();

console.log('🚀 Building Claude Vision Gallery...');
console.log(`📦 Version: ${version}`);

// Read and update index.html
let indexHtml = fs.readFileSync('index.html', 'utf8');

// Update CSS and JS references with cache-busting version
indexHtml = indexHtml.replace(/styles\.css\?v=[\d\.]+/g, `styles.css?v=${version}`);
indexHtml = indexHtml.replace(/gallery\.js\?v=[\d\.]+/g, `gallery.js?v=${version}`);

// Write updated index.html
fs.writeFileSync('index.html', indexHtml);
console.log('✅ Updated index.html with cache-busting');

// Read and update gallery.js
let galleryJs = fs.readFileSync('gallery.js', 'utf8');

// Replace Date.now() with fixed version for this build
galleryJs = galleryJs.replace(/\?v=\$\{Date\.now\(\)\}/g, `?v=${version}`);

// Write updated gallery.js
fs.writeFileSync('gallery.js', galleryJs);
console.log('✅ Updated gallery.js with cache-busting');

console.log('✨ Build complete!');
console.log('🌐 Ready to deploy with: wrangler pages deploy . --project-name=claude-vision');