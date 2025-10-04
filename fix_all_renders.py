#!/usr/bin/env python3
"""Fix all remaining render function stubs in app.js"""

with open('src/static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the implementations
deliverables_impl = '''    renderDeliverables() {
        const container = document.getElementById('deliverables-timeline');
        if (this.data.deliverables.length === 0) {
            this.showEmptyState('deliverables-timeline', 'tasks', 'No deliverables yet', 'Add your first deliverable to get started with timeline tracking');
            return;
        }

        container.innerHTML = this.data.deliverables.map(item => {
            const title = item.title || 'Untitled';
            const desc = item.description || '';
            const dueDate = item.due_date || 'No date';
            const phase = item.phase || 'Unassigned';
            const status = item.status || 'Not started';

            let card = '<div class="deliverable-card">';
            card += '<div class="deliverable-header">';
            card += '<h3>' + title + '</h3>';
            card += '<span class="status-badge status-' + status.toLowerCase().replace(' ', '-') + '">' + status + '</span>';
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
        }).join('');
    }'''

ai_tech_impl = '''    renderAITechnologies() {
        const container = document.getElementById('ai-tech-grid');
        if (this.data.aiTechnologies.length === 0) {
            this.showEmptyState('ai-tech-grid', 'robot', 'No AI technologies yet', 'Add your first AI technology to start building your comprehensive catalog');
            return;
        }

        container.innerHTML = this.data.aiTechnologies.map(tech => {
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
        }).join('');
    }'''

integrations_impl = '''    renderIntegrations() {
        const container = document.getElementById('integration-logs');
        if (this.data.integrations.length === 0) {
            this.showEmptyState('integration-logs', 'plug', 'No integration activity yet', 'Configure your first integration to see activity logs');
            return;
        }

        container.innerHTML = this.data.integrations.map(item => {
            const name = item.name || 'Untitled Integration';
            const type = item.integration_type || 'Unknown';
            const status = item.status || 'Inactive';
            const desc = item.description || 'No description';
            const endpoint = item.api_endpoint || '';

            let card = '<div class="integration-card">';
            card += '<div class="integration-header">';
            card += '<h3>' + name + '</h3>';
            card += '<span class="status-badge status-' + status.lower() + '">' + status + '</span>';
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
        }).join('');
    }'''

# Replace each stub - match the whole function including the closing brace
import re

# Pattern to match the stub functions
def replace_stub(pattern_name, new_impl):
    # Match from "renderX() {" to its closing "}"
    pattern = rf'    {pattern_name}\(\) \{{\s+const container[^}}]+container\.innerHTML = \'<div class="loading">Loading[^}}]+\}}\s+\}}'
    return re.sub(pattern, new_impl, content, flags=re.DOTALL)

content = replace_stub('renderDeliverables', deliverables_impl)
content = replace_stub('renderAITechnologies', ai_tech_impl)
content = replace_stub('renderIntegrations', integrations_impl)

with open('src/static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! All render functions implemented.")
print("- renderDeliverables()")
print("- renderAITechnologies()")
print("- renderIntegrations()")
