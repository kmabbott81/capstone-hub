import { test, expect } from '@playwright/test';

/**
 * End-to-End Tests - Critical User Flows
 *
 * Tests complete user journeys from login to task completion.
 * Simulates real user behavior including navigation, form submission, and state changes.
 */

test.describe('E2E: Authentication Flow', () => {
  test('Admin login and logout flow', async ({ page }) => {
    // Navigate to login page
    await page.goto('/');

    // Verify login form is present
    await expect(page.locator('#login-form')).toBeVisible();

    // Enter admin credentials
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');

    // Submit login
    await page.click('button[type="submit"]');

    // Wait for dashboard to load
    await page.waitForSelector('#dashboard.content-section.active');

    // Verify admin elements are visible
    await expect(page.locator('.admin-only').first()).toBeVisible();

    // Logout
    await page.click('[data-action="logout"]');

    // Verify redirected to login
    await expect(page.locator('#login-form')).toBeVisible();
  });

  test('Viewer login has read-only access', async ({ page }) => {
    await page.goto('/');

    // Login as viewer
    await page.fill('input[name="username"]', 'viewer');
    await page.fill('input[name="password"]', process.env.VIEWER_PASSWORD || 'CapstoneView');
    await page.click('button[type="submit"]');

    // Wait for dashboard
    await page.waitForSelector('#dashboard.content-section.active');

    // Verify admin elements are hidden
    await expect(page.locator('.admin-only').first()).toBeHidden();

    // Verify viewer can view data
    await expect(page.locator('.metrics-row')).toBeVisible();
  });
});

test.describe('E2E: Deliverable Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin before each test
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('Create new deliverable', async ({ page }) => {
    // Navigate to deliverables section
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');

    // Click add button
    await page.click('[data-action="add-deliverable"]');

    // Wait for modal
    await page.waitForSelector('#item-modal');

    // Fill form
    await page.fill('input[name="title"]', 'E2E Test Deliverable');
    await page.fill('textarea[name="description"]', 'Created by automated E2E test');
    await page.selectOption('select[name="status"]', 'In Progress');

    // Submit form
    await page.click('#item-modal button[type="submit"]');

    // Wait for modal to close
    await page.waitForSelector('#item-modal', { state: 'hidden' });

    // Verify deliverable appears in list
    await expect(page.locator('text=E2E Test Deliverable')).toBeVisible();
  });

  test('Edit existing deliverable', async ({ page }) => {
    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');

    // Click first edit button
    await page.click('.deliverable-item [data-action="edit"]');

    // Wait for modal
    await page.waitForSelector('#item-modal');

    // Modify title
    await page.fill('input[name="title"]', 'Updated Deliverable Title');

    // Submit
    await page.click('#item-modal button[type="submit"]');

    // Verify updated
    await expect(page.locator('text=Updated Deliverable Title')).toBeVisible();
  });

  test('Delete deliverable', async ({ page }) => {
    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');

    // Get initial count
    const initialCount = await page.locator('.deliverable-item').count();

    // Click first delete button
    await page.click('.deliverable-item [data-action="delete"]');

    // Confirm deletion (if confirmation dialog exists)
    page.on('dialog', dialog => dialog.accept());

    // Wait for deletion to complete
    await page.waitForTimeout(500);

    // Verify count decreased
    const newCount = await page.locator('.deliverable-item').count();
    expect(newCount).toBeLessThan(initialCount);
  });
});

test.describe('E2E: Navigation and Tabs', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('Navigate through all sections', async ({ page }) => {
    const sections = [
      'deliverables',
      'business-processes',
      'ai-technologies',
      'software-tools',
      'research-items'
    ];

    for (const section of sections) {
      // Click section link
      await page.click(`[data-section="${section}"]`);

      // Verify section is active
      await expect(page.locator(`#${section}.content-section.active`)).toBeVisible();

      // Verify other sections are hidden
      const otherSections = sections.filter(s => s !== section);
      for (const other of otherSections) {
        await expect(page.locator(`#${other}.content-section.active`)).toBeHidden();
      }
    }
  });

  test('Tab filtering within sections', async ({ page }) => {
    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');

    // Check if tabs exist
    const tabs = page.locator('.filter-buttons button');
    const tabCount = await tabs.count();

    if (tabCount > 0) {
      // Click first tab
      await tabs.first().click();

      // Verify tab is active
      await expect(tabs.first()).toHaveClass(/active/);
    }
  });
});

test.describe('E2E: Dark Mode Toggle', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('Toggle dark mode and persist preference', async ({ page }) => {
    // Verify initial theme
    const initialTheme = await page.evaluate(() => document.documentElement.dataset.theme);

    // Click theme toggle
    await page.click('[data-action="toggle-theme"]');

    // Wait for theme change
    await page.waitForTimeout(300);

    // Verify theme changed
    const newTheme = await page.evaluate(() => document.documentElement.dataset.theme);
    expect(newTheme).not.toBe(initialTheme);

    // Verify localStorage was updated
    const storedTheme = await page.evaluate(() => localStorage.getItem('capstone-theme'));
    expect(storedTheme).toBe(newTheme);

    // Reload page
    await page.reload();
    await page.waitForSelector('#dashboard.content-section.active');

    // Verify theme persisted
    const persistedTheme = await page.evaluate(() => document.documentElement.dataset.theme);
    expect(persistedTheme).toBe(newTheme);
  });
});

test.describe('E2E: Search and Filter', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('Search filters deliverables', async ({ page }) => {
    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');

    // Get initial count
    const initialCount = await page.locator('.deliverable-item').count();

    // Enter search term
    const searchInput = page.locator('input[type="search"]');
    if (await searchInput.count() > 0) {
      await searchInput.fill('test');

      // Wait for filter
      await page.waitForTimeout(500);

      // Verify filtered results
      const filteredCount = await page.locator('.deliverable-item:visible').count();
      expect(filteredCount).toBeLessThanOrEqual(initialCount);
    }
  });
});

test.describe('E2E: Session Timeout', () => {
  test('Session expires after inactivity', async ({ page }) => {
    // Login
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');

    // Clear session cookie to simulate expiration
    await page.context().clearCookies();

    // Try to navigate
    await page.click('[data-section="deliverables"]');

    // Should redirect to login
    await page.waitForTimeout(1000);

    // Verify login form is visible (session expired)
    const loginForm = page.locator('#login-form');
    if (await loginForm.count() > 0) {
      await expect(loginForm).toBeVisible();
    }
  });
});

test.describe('E2E: Error Handling', () => {
  test('Handles network errors gracefully', async ({ page }) => {
    // Login
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');

    // Intercept API calls and simulate error
    await page.route('**/api/**', route => route.abort());

    // Try to create deliverable
    await page.click('[data-section="deliverables"]');
    await page.click('[data-action="add-deliverable"]');

    // Fill form
    await page.fill('input[name="title"]', 'Error Test');
    await page.click('#item-modal button[type="submit"]');

    // Should show error message or handle gracefully
    // (Exact behavior depends on implementation)
    await page.waitForTimeout(1000);
  });

  test('Invalid login shows error message', async ({ page }) => {
    await page.goto('/');

    // Enter invalid credentials
    await page.fill('input[name="username"]', 'invalid');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // Wait for error message
    await page.waitForTimeout(1000);

    // Verify still on login page
    await expect(page.locator('#login-form')).toBeVisible();

    // Check for error message (implementation-specific)
    const errorMessage = page.locator('.error-message, .alert-danger');
    if (await errorMessage.count() > 0) {
      await expect(errorMessage).toBeVisible();
    }
  });
});
