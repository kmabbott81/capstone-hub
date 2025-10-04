# Phase 1B Implementation Guide: Edit Functions
**Version:** 0.37.0 (Planned)
**Estimated Effort:** 3-4 hours
**Status:** Ready to implement after Option 2 (live validation)

---

## Overview

Phase 1B completes the CRUD baseline by implementing edit/update functionality for the 5 remaining entity types. Business Processes already has this implemented - use it as the template.

---

## Implementation Pattern (Copy from Business Processes)

### Backend (Already Complete ✅)
All PUT endpoints already exist with `@require_admin` and `@csrf.protect`:
- PUT `/api/deliverables/<id>`
- PUT `/api/ai-technologies/<id>`
- PUT `/api/software-tools/<id>`
- PUT `/api/research-items/<id>`
- PUT `/api/integrations/<id>`

**No backend changes needed!**

---

## Frontend Implementation (5 Entities)

### 1. Deliverables Edit Function

**File:** `src/static/app.js`

**Add after line ~590 (after `saveDeliverable()`):**

```javascript
editDeliverable(id) {
    const deliverable = this.data.deliverables.find(d => d.id === id);
    if (!deliverable) return;

    this.openModal('Edit Deliverable', `
        <form id="edit-deliverable-form">
            <input type="hidden" id="edit-deliverable-id" value="${id}">

            <div class="form-group">
                <label for="edit-deliverable-title">Title *</label>
                <input type="text" id="edit-deliverable-title"
                       value="${escapeHTML(deliverable.title)}" required>
            </div>

            <div class="form-group">
                <label for="edit-deliverable-description">Description</label>
                <textarea id="edit-deliverable-description" rows="4">${escapeHTML(deliverable.description || '')}</textarea>
            </div>

            <div class="form-group">
                <label for="edit-deliverable-phase">Phase *</label>
                <select id="edit-deliverable-phase" required>
                    <option value="Foundation" ${deliverable.phase === 'Foundation' ? 'selected' : ''}>Foundation & Planning</option>
                    <option value="Research" ${deliverable.phase === 'Research' ? 'selected' : ''}>Research & Analysis</option>
                    <option value="Implementation" ${deliverable.phase === 'Implementation' ? 'selected' : ''}>Implementation</option>
                    <option value="Evaluation" ${deliverable.phase === 'Evaluation' ? 'selected' : ''}>Evaluation & Testing</option>
                    <option value="Final" ${deliverable.phase === 'Final' ? 'selected' : ''}>Final Report & Presentation</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-deliverable-due-date">Due Date</label>
                <input type="date" id="edit-deliverable-due-date"
                       value="${deliverable.due_date || ''}">
            </div>

            <div class="form-actions">
                <button type="button" data-action="close-modal" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Update Deliverable</button>
            </div>
        </form>
    `);

    document.getElementById('edit-deliverable-form').addEventListener('submit', (e) => {
        e.preventDefault();
        this.updateDeliverable(id);
    });
}

async updateDeliverable(id) {
    const title = document.getElementById('edit-deliverable-title').value;
    const description = document.getElementById('edit-deliverable-description').value;
    const phase = document.getElementById('edit-deliverable-phase').value;
    const dueDate = document.getElementById('edit-deliverable-due-date').value;

    try {
        const token = await getCSRFToken();
        const response = await fetch(`/api/deliverables/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                title: title,
                description: description,
                phase: phase,
                due_date: dueDate
            })
        });

        if (response.ok) {
            this.closeModal();
            await this.loadDeliverables();
            this.updateDashboard();
            showNotification('Deliverable updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update deliverable', 'error');
        }
    } catch (error) {
        console.error('Update error:', error);
        showNotification('Failed to update deliverable', 'error');
    }
}
```

---

### 2. AI Technologies Edit Function

**Add after line ~1065 (after `saveAITechnology()`):**

```javascript
editAITechnology(id) {
    const tech = this.data.aiTechnologies.find(t => t.id === id);
    if (!tech) return;

    this.openModal('Edit AI Technology', `
        <form id="edit-ai-tech-form">
            <input type="hidden" id="edit-ai-tech-id" value="${id}">

            <div class="form-group">
                <label for="edit-ai-tech-name">Name *</label>
                <input type="text" id="edit-ai-tech-name"
                       value="${escapeHTML(tech.name)}" required>
            </div>

            <div class="form-group">
                <label for="edit-ai-tech-category">Category *</label>
                <select id="edit-ai-tech-category" required>
                    <option value="Generative" ${tech.category === 'Generative' ? 'selected' : ''}>Generative AI</option>
                    <option value="Agentic" ${tech.category === 'Agentic' ? 'selected' : ''}>Agentic AI</option>
                    <option value="Embedded" ${tech.category === 'Embedded' ? 'selected' : ''}>Embedded AI</option>
                    <option value="Predictive" ${tech.category === 'Predictive' ? 'selected' : ''}>Predictive AI</option>
                    <option value="Computer Vision" ${tech.category === 'Computer Vision' ? 'selected' : ''}>Computer Vision</option>
                    <option value="NLP" ${tech.category === 'NLP' ? 'selected' : ''}>Natural Language Processing</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-ai-tech-provider">Provider</label>
                <input type="text" id="edit-ai-tech-provider"
                       value="${escapeHTML(tech.platform_provider || '')}">
            </div>

            <div class="form-group">
                <label for="edit-ai-tech-description">Description</label>
                <textarea id="edit-ai-tech-description" rows="4">${escapeHTML(tech.description || '')}</textarea>
            </div>

            <div class="form-actions">
                <button type="button" data-action="close-modal" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Update AI Technology</button>
            </div>
        </form>
    `);

    document.getElementById('edit-ai-tech-form').addEventListener('submit', (e) => {
        e.preventDefault();
        this.updateAITechnology(id);
    });
}

async updateAITechnology(id) {
    const name = document.getElementById('edit-ai-tech-name').value;
    const category = document.getElementById('edit-ai-tech-category').value;
    const provider = document.getElementById('edit-ai-tech-provider').value;
    const description = document.getElementById('edit-ai-tech-description').value;

    try {
        const token = await getCSRFToken();
        const response = await fetch(`/api/ai-technologies/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                name: name,
                category: category,
                platform_provider: provider,
                description: description
            })
        });

        if (response.ok) {
            this.closeModal();
            await this.loadAITechnologies();
            this.updateDashboard();
            showNotification('AI Technology updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update AI technology', 'error');
        }
    } catch (error) {
        console.error('Update error:', error);
        showNotification('Failed to update AI technology', 'error');
    }
}
```

---

### 3. Software Tools Edit Function

**Add after line ~1153 (after `saveSoftwareTool()`):**

```javascript
editSoftwareTool(id) {
    const tool = this.data.softwareTools.find(t => t.id === id);
    if (!tool) return;

    this.openModal('Edit Software Tool', `
        <form id="edit-tool-form">
            <input type="hidden" id="edit-tool-id" value="${id}">

            <div class="form-group">
                <label for="edit-tool-name">Name *</label>
                <input type="text" id="edit-tool-name"
                       value="${escapeHTML(tool.name)}" required>
            </div>

            <div class="form-group">
                <label for="edit-tool-category">Category *</label>
                <select id="edit-tool-category" required>
                    <option value="Core System" ${tool.category === 'Core System' ? 'selected' : ''}>Core System</option>
                    <option value="Optional Tool" ${tool.category === 'Optional Tool' ? 'selected' : ''}>Optional Tool</option>
                    <option value="Integration" ${tool.category === 'Integration' ? 'selected' : ''}>Integration Tool</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-tool-type">Tool Type *</label>
                <select id="edit-tool-type" required>
                    <option value="CRM" ${tool.tool_type === 'CRM' ? 'selected' : ''}>CRM</option>
                    <option value="Project Management" ${tool.tool_type === 'Project Management' ? 'selected' : ''}>Project Management</option>
                    <option value="Communication" ${tool.tool_type === 'Communication' ? 'selected' : ''}>Communication</option>
                    <option value="Analytics" ${tool.tool_type === 'Analytics' ? 'selected' : ''}>Analytics</option>
                    <option value="Development" ${tool.tool_type === 'Development' ? 'selected' : ''}>Development</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-tool-description">Description</label>
                <textarea id="edit-tool-description" rows="4">${escapeHTML(tool.description || '')}</textarea>
            </div>

            <div class="form-actions">
                <button type="button" data-action="close-modal" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Update Software Tool</button>
            </div>
        </form>
    `);

    document.getElementById('edit-tool-form').addEventListener('submit', (e) => {
        e.preventDefault();
        this.updateSoftwareTool(id);
    });
}

async updateSoftwareTool(id) {
    const name = document.getElementById('edit-tool-name').value;
    const category = document.getElementById('edit-tool-category').value;
    const toolType = document.getElementById('edit-tool-type').value;
    const description = document.getElementById('edit-tool-description').value;

    try {
        const token = await getCSRFToken();
        const response = await fetch(`/api/software-tools/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                name: name,
                category: category,
                tool_type: toolType,
                description: description
            })
        });

        if (response.ok) {
            this.closeModal();
            await this.loadSoftwareTools();
            this.updateDashboard();
            showNotification('Software tool updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update software tool', 'error');
        }
    } catch (error) {
        console.error('Update error:', error);
        showNotification('Failed to update software tool', 'error');
    }
}
```

---

### 4. Research Items Edit Function

**Add after line ~1239 (after `saveResearchItem()`):**

```javascript
editResearchItem(id) {
    const item = this.data.researchItems.find(r => r.id === id);
    if (!item) return;

    this.openModal('Edit Research Item', `
        <form id="edit-research-form">
            <input type="hidden" id="edit-research-id" value="${id}">

            <div class="form-group">
                <label for="edit-research-title">Title *</label>
                <input type="text" id="edit-research-title"
                       value="${escapeHTML(item.title)}" required>
            </div>

            <div class="form-group">
                <label for="edit-research-type">Research Type *</label>
                <select id="edit-research-type" required>
                    <option value="Primary" ${item.research_type === 'Primary' ? 'selected' : ''}>Primary Research</option>
                    <option value="Secondary" ${item.research_type === 'Secondary' ? 'selected' : ''}>Secondary Research</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-research-method">Research Method</label>
                <input type="text" id="edit-research-method"
                       value="${escapeHTML(item.research_method || '')}">
            </div>

            <div class="form-group">
                <label for="edit-research-description">Description</label>
                <textarea id="edit-research-description" rows="4">${escapeHTML(item.description || '')}</textarea>
            </div>

            <div class="form-actions">
                <button type="button" data-action="close-modal" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Update Research Item</button>
            </div>
        </form>
    `);

    document.getElementById('edit-research-form').addEventListener('submit', (e) => {
        e.preventDefault();
        this.updateResearchItem(id);
    });
}

async updateResearchItem(id) {
    const title = document.getElementById('edit-research-title').value;
    const researchType = document.getElementById('edit-research-type').value;
    const researchMethod = document.getElementById('edit-research-method').value;
    const description = document.getElementById('edit-research-description').value;

    try {
        const token = await getCSRFToken();
        const response = await fetch(`/api/research-items/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                title: title,
                research_type: researchType,
                research_method: researchMethod,
                description: description
            })
        });

        if (response.ok) {
            this.closeModal();
            await this.loadResearchItems();
            this.updateDashboard();
            showNotification('Research item updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update research item', 'error');
        }
    } catch (error) {
        console.error('Update error:', error);
        showNotification('Failed to update research item', 'error');
    }
}
```

---

### 5. Integrations Edit Function

**Add after line ~1327 (after `saveIntegration()`):**

```javascript
editIntegration(id) {
    const integration = this.data.integrations.find(i => i.id === id);
    if (!integration) return;

    this.openModal('Edit Integration', `
        <form id="edit-integration-form">
            <input type="hidden" id="edit-integration-id" value="${id}">

            <div class="form-group">
                <label for="edit-integration-name">Name *</label>
                <input type="text" id="edit-integration-name"
                       value="${escapeHTML(integration.name)}" required>
            </div>

            <div class="form-group">
                <label for="edit-integration-platform">Platform *</label>
                <select id="edit-integration-platform" required>
                    <option value="Notion" ${integration.platform === 'Notion' ? 'selected' : ''}>Notion</option>
                    <option value="Microsoft 365" ${integration.platform === 'Microsoft 365' ? 'selected' : ''}>Microsoft 365</option>
                    <option value="Google Workspace" ${integration.platform === 'Google Workspace' ? 'selected' : ''}>Google Workspace</option>
                    <option value="Other" ${integration.platform === 'Other' ? 'selected' : ''}>Other</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-integration-type">Integration Type *</label>
                <select id="edit-integration-type" required>
                    <option value="API" ${integration.integration_type === 'API' ? 'selected' : ''}>API</option>
                    <option value="Webhook" ${integration.integration_type === 'Webhook' ? 'selected' : ''}>Webhook</option>
                    <option value="OAuth" ${integration.integration_type === 'OAuth' ? 'selected' : ''}>OAuth</option>
                    <option value="Manual" ${integration.integration_type === 'Manual' ? 'selected' : ''}>Manual</option>
                </select>
            </div>

            <div class="form-group">
                <label for="edit-integration-purpose">Purpose</label>
                <textarea id="edit-integration-purpose" rows="3">${escapeHTML(integration.purpose || '')}</textarea>
            </div>

            <div class="form-actions">
                <button type="button" data-action="close-modal" class="btn-secondary">Cancel</button>
                <button type="submit" class="btn-primary">Update Integration</button>
            </div>
        </form>
    `);

    document.getElementById('edit-integration-form').addEventListener('submit', (e) => {
        e.preventDefault();
        this.updateIntegration(id);
    });
}

async updateIntegration(id) {
    const name = document.getElementById('edit-integration-name').value;
    const platform = document.getElementById('edit-integration-platform').value;
    const integrationType = document.getElementById('edit-integration-type').value;
    const purpose = document.getElementById('edit-integration-purpose').value;

    try {
        const token = await getCSRFToken();
        const response = await fetch(`/api/integrations/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': token
            },
            body: JSON.stringify({
                name: name,
                platform: platform,
                integration_type: integrationType,
                purpose: purpose
            })
        });

        if (response.ok) {
            this.closeModal();
            await this.loadIntegrations();
            this.updateDashboard();
            showNotification('Integration updated successfully!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.error || 'Failed to update integration', 'error');
        }
    } catch (error) {
        console.error('Update error:', error);
        showNotification('Failed to update integration', 'error');
    }
}
```

---

## Testing Checklist

After implementing each edit function:

- [ ] Edit button appears on card (already wired via event delegation)
- [ ] Click Edit → Modal opens with pre-filled data
- [ ] Modify fields → Click Update
- [ ] Modal closes automatically
- [ ] Card updates immediately with new data
- [ ] Page refresh → changes persist
- [ ] Dashboard counts remain accurate
- [ ] Console shows no errors
- [ ] CSRF token included in request (check Network tab)

---

## Deployment

```bash
# After implementing all 5 functions
git add src/static/app.js
git commit -m "Phase 1B: Complete edit functions for all entities

- Deliverables edit/update
- AI Technologies edit/update
- Software Tools edit/update
- Research Items edit/update
- Integrations edit/update

All use CSRF tokens and event delegation pattern

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push
railway up --service capstone-hub

# Tag the release
git tag -a v0.37.0 -m "Phase 1B Complete - Full CRUD for all entities"
git push origin v0.37.0
```

---

## Time Estimate Breakdown

- Deliverables: 30 minutes
- AI Technologies: 35 minutes
- Software Tools: 40 minutes
- Research Items: 30 minutes
- Integrations: 30 minutes
- Testing all 5: 45 minutes
- Deployment & verification: 20 minutes

**Total: 3.5 hours**

---

## Next After Phase 1B

With full CRUD complete, you'll have:
- ✅ Create operations (all 6 entities)
- ✅ Read operations (all 6 entities)
- ✅ Update operations (all 6 entities)
- ✅ Delete operations (all 6 entities)
- ✅ Server-side authorization
- ✅ CSRF protection
- ✅ Rate limiting
- ✅ Session timeout
- ✅ Database backups

**That's production-grade baseline CRUD.** Then move to Phase 2 (attachments, comments, search, export).
