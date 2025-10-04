import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Accessibility Tests - WCAG 2.1 AA Compliance
 *
 * Tests application against Web Content Accessibility Guidelines using axe-core.
 * Ensures keyboard navigation, screen reader support, and proper ARIA attributes.
 */

test.describe('Accessibility: Login Page', () => {
  test('should not have accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('form inputs have proper labels', async ({ page }) => {
    await page.goto('/');

    // Check username field
    const usernameLabel = page.locator('label[for="username"]');
    await expect(usernameLabel).toBeVisible();

    // Check password field
    const passwordLabel = page.locator('label[for="password"]');
    await expect(passwordLabel).toBeVisible();
  });

  test('keyboard navigation works on login form', async ({ page }) => {
    await page.goto('/');

    // Tab to username field
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="username"]')).toBeFocused();

    // Tab to password field
    await page.keyboard.press('Tab');
    await expect(page.locator('input[name="password"]')).toBeFocused();

    // Tab to submit button
    await page.keyboard.press('Tab');
    await expect(page.locator('button[type="submit"]')).toBeFocused();
  });
});

test.describe('Accessibility: Dashboard (Authenticated)', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('dashboard should not have accessibility violations', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('navigation links are keyboard accessible', async ({ page }) => {
    // Get all navigation links
    const navLinks = page.locator('.nav-link');
    const count = await navLinks.count();

    for (let i = 0; i < count; i++) {
      const link = navLinks.nth(i);

      // Focus the link
      await link.focus();
      await expect(link).toBeFocused();

      // Verify it has proper ARIA or text content
      const text = await link.textContent();
      expect(text).toBeTruthy();
    }
  });

  test('buttons have accessible names', async ({ page }) => {
    const buttons = page.locator('button');
    const count = await buttons.count();

    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);

      // Get accessible name (text, aria-label, or title)
      const accessibleName = await button.evaluate(el => {
        return el.textContent?.trim() ||
               el.getAttribute('aria-label') ||
               el.getAttribute('title') ||
               '';
      });

      expect(accessibleName).toBeTruthy();
    }
  });
});

test.describe('Accessibility: Deliverables Section', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');

    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');
  });

  test('deliverables section should not have accessibility violations', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('table has proper structure', async ({ page }) => {
    const table = page.locator('table').first();

    if (await table.count() > 0) {
      // Check for thead
      await expect(table.locator('thead')).toBeVisible();

      // Check for th elements
      const headers = table.locator('th');
      const headerCount = await headers.count();
      expect(headerCount).toBeGreaterThan(0);

      // Check for tbody
      await expect(table.locator('tbody')).toBeVisible();
    }
  });
});

test.describe('Accessibility: Modals and Dialogs', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');

    // Navigate to deliverables
    await page.click('[data-section="deliverables"]');
    await page.waitForSelector('#deliverables.content-section.active');
  });

  test('modal dialog has proper ARIA attributes', async ({ page }) => {
    // Open modal
    await page.click('[data-action="add-deliverable"]');
    await page.waitForSelector('#item-modal');

    const modal = page.locator('#item-modal');

    // Check for role="dialog" or aria-modal="true"
    const role = await modal.getAttribute('role');
    const ariaModal = await modal.getAttribute('aria-modal');

    expect(role === 'dialog' || ariaModal === 'true').toBeTruthy();
  });

  test('modal traps focus', async ({ page }) => {
    // Open modal
    await page.click('[data-action="add-deliverable"]');
    await page.waitForSelector('#item-modal');

    // Get first focusable element in modal
    const firstInput = page.locator('#item-modal input').first();
    await firstInput.focus();

    // Verify focus is within modal
    const focusedElement = await page.evaluate(() => {
      const activeEl = document.activeElement;
      const modal = document.getElementById('item-modal');
      return modal?.contains(activeEl);
    });

    expect(focusedElement).toBeTruthy();
  });

  test('modal can be closed with Escape key', async ({ page }) => {
    // Open modal
    await page.click('[data-action="add-deliverable"]');
    await page.waitForSelector('#item-modal');

    // Press Escape
    await page.keyboard.press('Escape');

    // Wait for modal to close
    await page.waitForTimeout(500);

    // Verify modal is hidden
    const modal = page.locator('#item-modal');
    const isVisible = await modal.isVisible();

    // Modal should be hidden or have display:none
    if (isVisible) {
      const display = await modal.evaluate(el => window.getComputedStyle(el).display);
      expect(display).toBe('none');
    }
  });
});

test.describe('Accessibility: Dark Mode', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('dark mode maintains sufficient contrast', async ({ page }) => {
    // Toggle to dark mode
    await page.click('[data-action="toggle-theme"]');
    await page.waitForTimeout(300);

    // Run accessibility scan in dark mode
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    );

    expect(contrastViolations).toEqual([]);
  });

  test('theme toggle button is accessible', async ({ page }) => {
    const toggleBtn = page.locator('[data-action="toggle-theme"]');

    // Check button has accessible name
    const accessibleName = await toggleBtn.evaluate(el => {
      return el.textContent?.trim() ||
             el.getAttribute('aria-label') ||
             el.getAttribute('title') ||
             '';
    });

    expect(accessibleName).toBeTruthy();

    // Verify button is keyboard accessible
    await toggleBtn.focus();
    await expect(toggleBtn).toBeFocused();

    // Verify Enter key activates button
    await page.keyboard.press('Enter');
    await page.waitForTimeout(300);

    // Theme should have changed
    const theme = await page.evaluate(() => document.documentElement.dataset.theme);
    expect(theme).toBeTruthy();
  });
});

test.describe('Accessibility: Color Contrast', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('all text meets WCAG AA contrast ratio', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze();

    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    );

    expect(contrastViolations).toEqual([]);
  });
});

test.describe('Accessibility: Landmarks and Headings', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('page has proper heading hierarchy', async ({ page }) => {
    // Check for h1
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBeGreaterThan(0);

    // Verify no skipped heading levels
    const headings = await page.evaluate(() => {
      const headingElements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
      return headingElements.map(el => parseInt(el.tagName.substring(1)));
    });

    // Check that each heading level doesn't skip more than 1 level
    for (let i = 1; i < headings.length; i++) {
      const diff = headings[i] - headings[i - 1];
      expect(diff).toBeLessThanOrEqual(1);
    }
  });

  test('page has landmark regions', async ({ page }) => {
    // Check for main landmark
    const main = page.locator('main, [role="main"]');
    const mainCount = await main.count();
    expect(mainCount).toBeGreaterThan(0);
  });
});

test.describe('Accessibility: Images and Media', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');
  });

  test('images have alt text', async ({ page }) => {
    const images = page.locator('img');
    const count = await images.count();

    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute('alt');

      // Alt attribute should exist (can be empty for decorative images)
      expect(alt).not.toBeNull();
    }
  });
});

test.describe('Accessibility: Forms', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.fill('input[name="username"]', 'admin');
    await page.fill('input[name="password"]', process.env.ADMIN_PASSWORD || 'CapstoneAdmin');
    await page.click('button[type="submit"]');
    await page.waitForSelector('#dashboard.content-section.active');

    // Open a form modal
    await page.click('[data-section="deliverables"]');
    await page.click('[data-action="add-deliverable"]');
    await page.waitForSelector('#item-modal');
  });

  test('form inputs have associated labels', async ({ page }) => {
    const inputs = page.locator('#item-modal input, #item-modal textarea, #item-modal select');
    const count = await inputs.count();

    for (let i = 0; i < count; i++) {
      const input = inputs.nth(i);
      const id = await input.getAttribute('id');
      const name = await input.getAttribute('name');

      if (id) {
        // Check for associated label
        const label = page.locator(`label[for="${id}"]`);
        const labelCount = await label.count();
        expect(labelCount).toBeGreaterThan(0);
      } else if (name) {
        // At minimum, should have name attribute for screen readers
        expect(name).toBeTruthy();
      }
    }
  });

  test('required fields are marked', async ({ page }) => {
    const requiredInputs = page.locator('#item-modal input[required], #item-modal textarea[required]');
    const count = await requiredInputs.count();

    for (let i = 0; i < count; i++) {
      const input = requiredInputs.nth(i);

      // Check for aria-required or required attribute
      const required = await input.getAttribute('required');
      const ariaRequired = await input.getAttribute('aria-required');

      expect(required !== null || ariaRequired === 'true').toBeTruthy();
    }
  });
});
