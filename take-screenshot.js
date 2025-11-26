const puppeteer = require('puppeteer');
const path = require('path');

async function takeScreenshot() {
  console.log('📸 Starting screenshot capture...');
  
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // Set viewport size
  await page.setViewport({
    width: 1400,
    height: 1000,
    deviceScaleFactor: 2
  });
  
  try {
    // Navigate to the app
    console.log('🌐 Loading http://localhost:3000...');
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle0',
      timeout: 30000
    });
    
    // Wait for content to load
    await page.waitForSelector('.header', { timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for any animations
    
    // Take screenshot
    const screenshotPath = path.join(__dirname, 'screenshot.png');
    await page.screenshot({
      path: screenshotPath,
      fullPage: true,
      type: 'png'
    });
    
    console.log('✅ Screenshot saved to:', screenshotPath);
    
  } catch (error) {
    console.error('❌ Error taking screenshot:', error.message);
    console.log('💡 Make sure your app is running on http://localhost:3000');
    process.exit(1);
  } finally {
    await browser.close();
  }
}

takeScreenshot();
