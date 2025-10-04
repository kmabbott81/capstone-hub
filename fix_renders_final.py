#!/usr/bin/env python3
"""Apply all 3 render function fixes correctly"""
import sys

with open('src/static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Replace renderDeliverables stub
old_deliverables = """        // Render deliverables timeline here
        container.innerHTML = '<div class="loading">Loading deliverables...</div>';"""

new_deliverables = """        container.innerHTML = this.data.deliverables.map(item => {
            const title = item.title || 'Untitled';
            const desc = item.description || '';
            const dueDate = item.due_date || 'No date';
            const phase = item.phase || 'Unassigned';
            const status = item.status || 'Not started';

            let card = '<div class="deliverable-card">';
            card += '<div class="deliverable-header">';
            card += '<h3>' + title + '</h3>';
            card += '<span class="status-badge status-' + status.toLowerCase().replace(/\\s+/g, '-') + '">' + status + '</span>';
            card += '</div>';
            card += '<div class="deliverable-body">';
            card += '<div class="field"><strong>Phase:</strong> ' + phase + '</div>';
            card += '<div class="field"><strong>Due Date:</strong> ' + dueDate + '</div>';
            if (desc) card += '<div class="field"><strong>Description:</strong> ' + desc + '</div>';
            card += '</div>';
            card += '<div class="deliverable-footer admin-only">';
            card += '<button class="btn-secondary btn-sm" onclick="capstoneHub.editDeliverable(' + item.id + ')"><i class="fas fa-edit"></i> Edit</button>';
            card += '<button class="btn-danger btn-sm" onclick="capstoneHub.deleteDeliverable(' + item.id + ')"><i class="fas fa-trash"></i> Delete</button>';
            card += '</div></div>';
            return card;
        }).join('');"""

# Fix 2: Replace renderAITechnologies stub
old_ai_tech = """        // Render AI technologies grid here
        container.innerHTML = '<div class="loading">Loading AI technologies...</div>';"""

new_ai_tech = """        container.innerHTML = this.data.aiTechnologies.map(tech => {
            const name = tech.name || 'Untitled';
            const category = tech.category || 'Uncategorized';
            const desc = tech.description || 'No description';
            const useCase = tech.use_case || '';
            const maturity = tech.maturity_level || 'Unknown';

            let card = '<div class="tech-card">';
            card += '<div class="tech-header">';
            card += '<h3>' + name + '</h3>';
            card += '<span class="tech-badge">' + category + '</span>';
            card += '</div>';
            card += '<div class="tech-body">';
            card += '<div class="field"><strong>Maturity:</strong> ' + maturity + '</div>';
            card += '<div class="field"><strong>Description:</strong> ' + desc + '</div>';
            if (useCase) card += '<div class="field"><strong>Use Case:</strong> ' + useCase + '</div>';
            card += '</div>';
            card += '<div class="tech-footer admin-only">';
            card += '<button class="btn-secondary btn-sm" onclick="capstoneHub.editAITechnology(' + tech.id + ')"><i class="fas fa-edit"></i> Edit</button>';
            card += '<button class="btn-danger btn-sm" onclick="capstoneHub.deleteAITechnology(' + tech.id + ')"><i class="fas fa-trash"></i> Delete</button>';
            card += '</div></div>';
            return card;
        }).join('');"""

# Fix 3: Replace renderIntegrations stub
old_integrations = """        // Render integration logs here
        container.innerHTML = '<div class="loading">Loading integration logs...</div>';"""

new_integrations = """        container.innerHTML = this.data.integrations.map(item => {
            const name = item.name || 'Untitled Integration';
            const type = item.integration_type || 'Unknown';
            const status = item.status || 'Inactive';
            const desc = item.description || 'No description';
            const endpoint = item.api_endpoint || '';

            let card = '<div class="integration-card">';
            card += '<div class="integration-header">';
            card += '<h3>' + name + '</h3>';
            card += '<span class="status-badge status-' + status.toLowerCase() + '">' + status + '</span>';
            card += '</div>';
            card += '<div class="integration-body">';
            card += '<div class="field"><strong>Type:</strong> ' + type + '</div>';
            card += '<div class="field"><strong>Description:</strong> ' + desc + '</div>';
            if (endpoint) card += '<div class="field"><strong>Endpoint:</strong> ' + endpoint + '</div>';
            card += '</div>';
            card += '<div class="integration-footer admin-only">';
            card += '<button class="btn-secondary btn-sm" onclick="capstoneHub.editIntegration(' + item.id + ')"><i class="fas fa-edit"></i> Edit</button>';
            card += '<button class="btn-danger btn-sm" onclick="capstoneHub.deleteIntegration(' + item.id + ')"><i class="fas fa-trash"></i> Delete</button>';
            card += '</div></div>';
            return card;
        }).join('');"""

# Apply replacements
if old_deliverables not in content:
    print("ERROR: Deliverables stub not found!")
    sys.exit(1)

if old_ai_tech not in content:
    print("ERROR: AI Technologies stub not found!")
    sys.exit(1)

if old_integrations not in content:
    print("ERROR: Integrations stub not found!")
    sys.exit(1)

content = content.replace(old_deliverables, new_deliverables)
content = content.replace(old_ai_tech, new_ai_tech)
content = content.replace(old_integrations, new_integrations)

with open('src/static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ All 3 render functions replaced successfully!")
print("   - renderDeliverables()")
print("   - renderAITechnologies()")
print("   - renderIntegrations()")
