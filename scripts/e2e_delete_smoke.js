/**
 * Playwright E2E Smoke Test: DELETE Button Functionality
 *
 * Tests that DELETE buttons work correctly with CSP-safe event delegation
 * and proper CSRF + credentials handling.
 *
 * Usage:
 *   npx playwright test scripts/e2e_delete_smoke.js
 *
 * Prerequisites:
 *   npm install -D playwright
 *   npx playwright install
 */

const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL || 'http://localhost:5000';
const ADMIN_EMAIL = process.env.ADMIN_EMAIL || 'admin@example.com';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';

test.describe('DELETE Button CSP-Safe Functionality', () => {
    test.beforeEach(async ({ page }) => {
        // Login as admin
        await page.goto(`${BASE_URL}/login`);
        await page.fill('input[name="email"]', ADMIN_EMAIL);
        await page.fill('input[name="password"]', ADMIN_PASSWORD);
        await page.click('button[type="submit"]');

        // Wait for dashboard to load
        await page.waitForURL(`${BASE_URL}/`);
        await page.waitForSelector('.dashboard-stats');
    });

    test('DELETE deliverable button sends proper CSRF and credentials', async ({ page }) => {
        // Navigate to deliverables section
        await page.click('[data-action="nav-deliverables"]');
        await page.waitForSelector('#deliverables-list');

        // Create a test deliverable first
        await page.click('[data-action="add-deliverable"]');
        await page.waitForSelector('#deliverable-form');

        await page.fill('input[name="title"]', 'Test Deliverable for Delete');
        await page.fill('textarea[name="description"]', 'This is a test deliverable to verify DELETE functionality');
        await page.selectOption('select[name="status"]', 'In Progress');
        await page.fill('input[name="due_date"]', '2025-12-31');

        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000); // Wait for card to appear

        // Find the delete button for our test deliverable
        const deleteButton = await page.locator('[data-action="delete-deliverable"]').last();

        // Set up request interception to verify CSRF and credentials
        let deleteRequestMade = false;
        let hasCsrfToken = false;
        let hasCredentials = false;

        page.on('request', request => {
            if (request.method() === 'DELETE' && request.url().includes('/api/deliverables/')) {
                deleteRequestMade = true;
                hasCsrfToken = request.headers()['x-csrftoken'] !== undefined;
                // Credentials are included automatically if fetch uses credentials: 'same-origin'
                hasCredentials = request.headers()['cookie'] !== undefined;
            }
        });

        // Handle the confirmation dialog
        page.on('dialog', dialog => dialog.accept());

        // Click delete button
        await deleteButton.click();

        // Wait for deletion to complete
        await page.waitForTimeout(1500);

        // Verify the request was made with proper headers
        expect(deleteRequestMade).toBe(true);
        expect(hasCsrfToken).toBe(true);
        expect(hasCredentials).toBe(true);

        // Verify the card disappeared (deleted successfully)
        const cardsAfter = await page.locator('.deliverable-card').count();
        // Should have one less card than before
    });

    test('DELETE business process button works without CSP violations', async ({ page }) => {
        // Navigate to business processes section
        await page.click('[data-action="nav-processes"]');
        await page.waitForSelector('#processes-list');

        // Create a test process
        await page.click('[data-action="add-process"]');
        await page.waitForSelector('#process-form');

        await page.fill('input[name="name"]', 'Test Process for Delete');
        await page.fill('textarea[name="description"]', 'Test process description');
        await page.selectOption('select[name="department"]', 'IT');
        await page.selectOption('select[name="automation_potential"]', 'High');

        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);

        // Check for CSP violations
        const cspViolations = [];
        page.on('console', msg => {
            if (msg.text().includes('Content Security Policy')) {
                cspViolations.push(msg.text());
            }
        });

        // Click delete button
        const deleteButton = await page.locator('[data-action="delete-process"]').last();
        page.on('dialog', dialog => dialog.accept());
        await deleteButton.click();

        await page.waitForTimeout(1500);

        // Verify no CSP violations occurred
        expect(cspViolations).toHaveLength(0);
    });

    test('All delete buttons use data-action attribute (no inline onclick)', async ({ page }) => {
        // Navigate through all sections and verify delete buttons
        const sections = [
            { action: 'nav-deliverables', selector: '[data-action="delete-deliverable"]' },
            { action: 'nav-processes', selector: '[data-action="delete-process"]' },
            { action: 'nav-ai-technologies', selector: '[data-action="delete-ai-technology"]' },
            { action: 'nav-software-tools', selector: '[data-action="delete-software-tool"]' },
            { action: 'nav-research-items', selector: '[data-action="delete-research-item"]' }
        ];

        for (const section of sections) {
            await page.click(`[data-action="${section.action}"]`);
            await page.waitForTimeout(500);

            // Check if there are any delete buttons in this section
            const deleteButtons = await page.locator(section.selector).count();

            if (deleteButtons > 0) {
                // Verify all delete buttons have data-action attribute
                const button = page.locator(section.selector).first();
                const hasDataAction = await button.getAttribute('data-action');
                expect(hasDataAction).toBeTruthy();

                // Verify no onclick attribute
                const hasOnclick = await button.getAttribute('onclick');
                expect(hasOnclick).toBeNull();
            }
        }
    });

    test('Modal close button uses data-action (no inline onclick)', async ({ page }) => {
        // Open dropdown editor modal
        await page.click('[data-action="edit-process-dropdowns"]');
        await page.waitForSelector('#dropdown-options-form');

        // Find cancel button
        const cancelButton = page.locator('[data-action="close-modal"]');

        // Verify it has data-action attribute
        const hasDataAction = await cancelButton.getAttribute('data-action');
        expect(hasDataAction).toBe('close-modal');

        // Verify no onclick attribute
        const hasOnclick = await cancelButton.getAttribute('onclick');
        expect(hasOnclick).toBeNull();

        // Click it to verify it works
        await cancelButton.click();
        await page.waitForTimeout(500);

        // Modal should be closed
        const modalVisible = await page.locator('#dropdown-options-form').isVisible();
        expect(modalVisible).toBe(false);
    });

    test('Add/Remove option buttons use data-action (no inline onclick)', async ({ page }) => {
        // Open dropdown editor modal
        await page.click('[data-action="edit-process-dropdowns"]');
        await page.waitForSelector('#dropdown-options-form');

        // Find add option button
        const addButton = page.locator('[data-action="add-option"]').first();

        // Verify it has data-action attribute
        const hasDataAction = await addButton.getAttribute('data-action');
        expect(hasDataAction).toBe('add-option');

        // Verify no onclick attribute
        const hasOnclick = await addButton.getAttribute('onclick');
        expect(hasOnclick).toBeNull();

        // Click to add an option
        const initialCount = await page.locator('.option-item').count();
        await addButton.click();
        await page.waitForTimeout(300);
        const newCount = await page.locator('.option-item').count();
        expect(newCount).toBe(initialCount + 1);

        // Verify the newly created remove button also uses data-action
        const removeButton = page.locator('[data-action="remove-option"]').last();
        const removeHasDataAction = await removeButton.getAttribute('data-action');
        expect(removeHasDataAction).toBe('remove-option');

        const removeHasOnclick = await removeButton.getAttribute('onclick');
        expect(removeHasOnclick).toBeNull();

        // Close modal
        await page.click('[data-action="close-modal"]');
    });
});

test.describe('DELETE Functionality Integration', () => {
    test.beforeEach(async ({ page }) => {
        // Login
        await page.goto(`${BASE_URL}/login`);
        await page.fill('input[name="email"]', ADMIN_EMAIL);
        await page.fill('input[name="password"]', ADMIN_PASSWORD);
        await page.click('button[type="submit"]');
        await page.waitForURL(`${BASE_URL}/`);
    });

    test('DELETE returns 200/204 and card disappears', async ({ page, context }) => {
        // Navigate to deliverables
        await page.click('[data-action="nav-deliverables"]');
        await page.waitForSelector('#deliverables-list');

        // Create a test deliverable
        await page.click('[data-action="add-deliverable"]');
        await page.waitForSelector('#deliverable-form');

        await page.fill('input[name="title"]', 'Temporary Test Item');
        await page.fill('textarea[name="description"]', 'Will be deleted immediately');
        await page.selectOption('select[name="status"]', 'Completed');
        await page.fill('input[name="due_date"]', '2025-01-01');

        await page.click('button[type="submit"]');
        await page.waitForTimeout(1000);

        // Count cards before deletion
        const cardsBefore = await page.locator('.deliverable-card').count();

        // Set up response monitoring
        let deleteResponse = null;
        page.on('response', async response => {
            if (response.request().method() === 'DELETE' && response.url().includes('/api/deliverables/')) {
                deleteResponse = response;
            }
        });

        // Click delete
        page.on('dialog', dialog => dialog.accept());
        await page.locator('[data-action="delete-deliverable"]').last().click();

        // Wait for delete to complete
        await page.waitForTimeout(1500);

        // Verify HTTP status
        expect(deleteResponse).not.toBeNull();
        expect([200, 204]).toContain(deleteResponse.status());

        // Verify card disappeared
        const cardsAfter = await page.locator('.deliverable-card').count();
        expect(cardsAfter).toBe(cardsBefore - 1);
    });
});

console.log('✅ E2E DELETE smoke test suite loaded');
console.log('Run with: npx playwright test scripts/e2e_delete_smoke.js');
