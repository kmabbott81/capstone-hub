import { test, expect } from '@playwright/test';

/**
 * Visual Regression Tests
 *
 * Captures snapshots of key pages and detects pixel-level changes.
 * Snapshots are stored in ui_snapshots/ and compared on each run.
 *
 * To approve new baselines: npm run test:update-snapshots
 */

test.describe('Visual Regression - Pages', () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin for full access
    await page.goto('/login.html');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'TestAdmin123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('/');
  });

  test('Dashboard page matches snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForSelector('#dashboard.content-section.active');

    // Wait for metrics to load
    await page.waitForSelector('.metrics-row');

    await expect(page).toHaveScreenshot('dashboard.png', {
      fullPage: true,
      maxDiffPixels: 100, // Allow small rendering differences
    });
  });

  test('Business Processes page matches snapshot', async ({ page }) => {
    await page.goto('/#processes');
    await page.waitForSelector('#processes.content-section.active');

    await expect(page).toHaveScreenshot('business-processes.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('Deliverables Timeline page matches snapshot', async ({ page }) => {
    await page.goto('/#deliverables');
    await page.waitForSelector('#deliverables.content-section.active');

    await expect(page).toHaveScreenshot('deliverables.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('AI Technologies page matches snapshot', async ({ page }) => {
    await page.goto('/#ai-technologies');
    await page.waitForSelector('#ai-technologies.content-section.active');

    await expect(page).toHaveScreenshot('ai-technologies.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('Research Management page matches snapshot', async ({ page }) => {
    await page.goto('/#research');
    await page.waitForSelector('#research.content-section.active');

    await expect(page).toHaveScreenshot('research.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('Integrations page matches snapshot', async ({ page }) => {
    await page.goto('/#integrations');
    await page.waitForSelector('#integrations.content-section.active');

    await expect(page).toHaveScreenshot('integrations.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });
});

test.describe('Visual Regression - Dark Mode', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login.html');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'TestAdmin123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('/');
  });

  test('Dashboard in dark mode matches snapshot', async ({ page }) => {
    // Toggle dark mode
    await page.click('[data-action="toggle-theme"]');

    // Wait for theme to apply
    await page.waitForTimeout(200);

    await expect(page).toHaveScreenshot('dashboard-dark.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });
});

test.describe('Visual Regression - Components', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login.html');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'TestAdmin123!');
    await page.click('button[type="submit"]');
    await page.waitForURL('/');
  });

  test('Navigation sidebar matches snapshot', async ({ page }) => {
    const sidebar = page.locator('.sidebar');
    await expect(sidebar).toHaveScreenshot('sidebar.png');
  });

  test('Metric cards match snapshot', async ({ page }) => {
    const metricsRow = page.locator('.metrics-row');
    await expect(metricsRow).toHaveScreenshot('metrics.png');
  });
});
