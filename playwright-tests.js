const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Test configuration
const BASE_URL = 'http://localhost:8000';
const SCREENSHOTS_DIR = path.join(__dirname, 'screenshots');

// Ensure screenshots directory exists
if (!fs.existsSync(SCREENSHOTS_DIR)) {
    fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
}

// Test suite
async function runTests() {
    console.log('🧪 Starting Playwright E2E Tests for Claude Vision Gallery\n');
    
    const browser = await chromium.launch();
    const context = await browser.newContext();
    const page = await context.newPage();
    
    let passedTests = 0;
    let failedTests = 0;
    const results = [];
    
    // Helper function to run a test
    async function test(name, fn) {
        try {
            console.log(`Running: ${name}`);
            await fn();
            console.log(`✅ ${name}\n`);
            passedTests++;
            results.push({ name, status: 'passed' });
        } catch (error) {
            console.error(`❌ ${name}`);
            console.error(`   Error: ${error.message}\n`);
            failedTests++;
            results.push({ name, status: 'failed', error: error.message });
        }
    }
    
    // Test 1: Page loads successfully
    await test('Page loads with correct title', async () => {
        await page.goto(BASE_URL);
        const title = await page.title();
        if (title !== 'Claude Vision Gallery - How AI Sees the World') {
            throw new Error(`Expected title "Claude Vision Gallery - How AI Sees the World", got "${title}"`);
        }
    });
    
    // Test 2: Hero section is visible
    await test('Hero section displays correctly', async () => {
        const heroTitle = await page.textContent('.hero-title');
        if (!heroTitle.includes('How Claude Code Sees the World')) {
            throw new Error('Hero title not found or incorrect');
        }
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'hero-section.png'),
            fullPage: false 
        });
    });
    
    // Test 3: Navigation works
    await test('Navigation links scroll to sections', async () => {
        // Click Gallery link
        await page.click('a[href="#gallery"]');
        await page.waitForTimeout(1000); // Wait for smooth scroll
        
        // Check if gallery section is in viewport
        const galleryVisible = await page.isVisible('#gallery');
        if (!galleryVisible) {
            throw new Error('Gallery section not visible after navigation');
        }
    });
    
    // Test 4: All gallery images load
    await test('All 5 gallery images load successfully', async () => {
        const images = await page.$$('.gallery-item img');
        if (images.length !== 5) {
            throw new Error(`Expected 5 gallery images, found ${images.length}`);
        }
        
        // Check each image loads
        for (let i = 0; i < images.length; i++) {
            const imgLoaded = await images[i].evaluate(img => img.complete && img.naturalHeight !== 0);
            if (!imgLoaded) {
                throw new Error(`Gallery image ${i + 1} failed to load`);
            }
        }
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'gallery-section.png'),
            fullPage: false 
        });
    });
    
    // Test 5: Lightbox functionality
    await test('Lightbox opens and closes correctly', async () => {
        // Click first gallery item
        await page.click('.gallery-item:first-child');
        await page.waitForTimeout(500);
        
        // Check lightbox is visible
        const lightboxVisible = await page.isVisible('.lightbox.active');
        if (!lightboxVisible) {
            throw new Error('Lightbox did not open');
        }
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'lightbox-open.png') 
        });
        
        // Close lightbox
        await page.click('.lightbox-close');
        await page.waitForTimeout(500);
        
        // Check lightbox is hidden
        const lightboxHidden = await page.isHidden('.lightbox.active');
        if (!lightboxHidden) {
            throw new Error('Lightbox did not close');
        }
    });
    
    // Test 6: Responsive design - Mobile
    await test('Responsive design works on mobile', async () => {
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto(BASE_URL);
        await page.waitForTimeout(1000);
        
        // Check if gallery grid is single column
        const galleryGrid = await page.$('.gallery-grid');
        const gridStyle = await galleryGrid.evaluate(el => window.getComputedStyle(el).gridTemplateColumns);
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'mobile-view.png'),
            fullPage: true 
        });
        
        // Reset viewport
        await page.setViewportSize({ width: 1280, height: 720 });
    });
    
    // Test 7: Responsive design - Tablet
    await test('Responsive design works on tablet', async () => {
        await page.setViewportSize({ width: 768, height: 1024 });
        await page.goto(BASE_URL);
        await page.waitForTimeout(1000);
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'tablet-view.png'),
            fullPage: true 
        });
        
        // Reset viewport
        await page.setViewportSize({ width: 1280, height: 720 });
    });
    
    // Test 8: Process section displays
    await test('Process section displays all steps', async () => {
        await page.goto(BASE_URL);
        await page.click('a[href="#process"]');
        await page.waitForTimeout(1000);
        
        const processSteps = await page.$$('.process-step');
        if (processSteps.length !== 3) {
            throw new Error(`Expected 3 process steps, found ${processSteps.length}`);
        }
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'process-section.png') 
        });
    });
    
    // Test 9: About section statistics
    await test('About section displays statistics', async () => {
        await page.goto(BASE_URL);
        await page.click('a[href="#about"]');
        await page.waitForTimeout(1000);
        
        const stats = await page.$$('.stat');
        if (stats.length !== 3) {
            throw new Error(`Expected 3 stats, found ${stats.length}`);
        }
    });
    
    // Test 10: No horizontal scroll
    await test('No horizontal scroll on any viewport', async () => {
        await page.goto(BASE_URL);
        
        const hasHorizontalScroll = await page.evaluate(() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        });
        
        if (hasHorizontalScroll) {
            throw new Error('Horizontal scroll detected');
        }
    });
    
    // Test 11: Full page screenshot
    await test('Full page renders correctly', async () => {
        await page.goto(BASE_URL);
        await page.waitForTimeout(2000); // Let animations complete
        
        await page.screenshot({ 
            path: path.join(SCREENSHOTS_DIR, 'full-page.png'),
            fullPage: true 
        });
    });
    
    // Test 12: Performance metrics
    await test('Page loads with acceptable performance', async () => {
        const metrics = await page.evaluate(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            return {
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                loadComplete: navigation.loadEventEnd - navigation.loadEventStart
            };
        });
        
        console.log(`   DOM Content Loaded: ${metrics.domContentLoaded}ms`);
        console.log(`   Load Complete: ${metrics.loadComplete}ms`);
        
        if (metrics.loadComplete > 3000) {
            throw new Error(`Page load time ${metrics.loadComplete}ms exceeds 3000ms threshold`);
        }
    });
    
    // Cleanup
    await browser.close();
    
    // Generate test report
    const report = {
        timestamp: new Date().toISOString(),
        totalTests: passedTests + failedTests,
        passed: passedTests,
        failed: failedTests,
        results: results,
        screenshotsGenerated: fs.readdirSync(SCREENSHOTS_DIR).filter(f => f.endsWith('.png')).length
    };
    
    fs.writeFileSync(
        path.join(__dirname, 'playwright-test-report.json'),
        JSON.stringify(report, null, 2)
    );
    
    // Summary
    console.log('\n📊 Test Summary:');
    console.log(`   Total Tests: ${report.totalTests}`);
    console.log(`   ✅ Passed: ${report.passed}`);
    console.log(`   ❌ Failed: ${report.failed}`);
    console.log(`   📸 Screenshots: ${report.screenshotsGenerated}`);
    console.log(`\n📁 Screenshots saved to: ${SCREENSHOTS_DIR}`);
    console.log(`📄 Report saved to: playwright-test-report.json`);
    
    // Exit with appropriate code
    process.exit(failedTests > 0 ? 1 : 0);
}

// Check if Playwright is installed
try {
    require.resolve('playwright');
    runTests().catch(console.error);
} catch (error) {
    console.error('❌ Playwright is not installed!');
    console.error('Please run: npm install playwright');
    process.exit(1);
}