import { defineConfig, devices } from '@playwright/test';

/**
 * Total Product Audit (TPA) - Playwright Configuration
 *
 * Comprehensive test suite covering:
 * - Visual regression
 * - E2E user flows
 * - Security (CSRF, cookies, headers)
 * - Accessibility (axe-core)
 * - Performance
 */

export default defineConfig({
  testDir: './tests/playwright',

  /* Maximum time one test can run for */
  timeout: 30 * 1000,

  /* Run tests in files in parallel */
  fullyParallel: true,

  /* Fail the build on CI if you accidentally left test.only */
  forbidOnly: !!process.env.CI,

  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,

  /* Opt out of parallel tests on CI */
  workers: process.env.CI ? 1 : undefined,

  /* Reporter to use */
  reporter: process.env.CI ? [
    ['html', { outputFolder: 'artifacts/playwright-report' }],
    ['json', { outputFile: 'artifacts/playwright-results.json' }],
    ['junit', { outputFile: 'artifacts/junit.xml' }]
  ] : 'html',

  /* Shared settings for all projects */
  use: {
    /* Base URL to use in actions like `await page.goto('/')` */
    baseURL: process.env.BASE_URL || 'http://localhost:5000',

    /* Collect trace when retrying the failed test */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',

    /* Video on failure */
    video: 'retain-on-failure',

    /* Timeout for each action */
    actionTimeout: 10 * 1000,

    /* Ignore HTTPS errors in dev */
    ignoreHTTPSErrors: !process.env.CI,
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    // Uncomment to test on other browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },

    /* Test against mobile viewports */
    // {
    //   name: 'Mobile Chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
  ],

  /* Run your local dev server before starting the tests */
  webServer: process.env.CI ? undefined : {
    command: 'python src/main.py',
    url: 'http://localhost:5000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
    env: {
      FLASK_ENV: 'development',
      ADMIN_PASSWORD: 'TestAdmin123!',
      VIEWER_PASSWORD: 'TestViewer123!',
      SECRET_KEY: 'test-secret-key-for-playwright-only',
      ENABLE_DEBUG_ROUTES: '0',
    },
  },

  /* Folder for test artifacts */
  outputDir: 'artifacts/playwright-screenshots',
});
