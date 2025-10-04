// Render function implementations to replace stubs

// 1. DELIVERABLES RENDER (replace line 271-279)
    renderDeliverables() {
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
            card += '<span class="status-badge status-' + status.toLowerCase().replace(/\s+/g, '-') + '">' + status + '</span>';
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
    }

// 2. AI TECHNOLOGIES RENDER (replace line 320-328)
    renderAITechnologies() {
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
    }

// 3. RESEARCH ITEMS RENDER (replace line 352-360)
    renderResearchItems() {
        const container = document.getElementById('research-content');
        if (this.data.researchItems.length === 0) {
            this.showEmptyState('research-content', 'search', 'No research items yet', 'Add your first research item to begin comprehensive documentation and tracking');
            return;
        }

        container.innerHTML = this.data.researchItems.map(item => {
            const title = item.title || 'Untitled';
            const type = item.research_type || 'General';
            const method = item.research_method || 'Not specified';
            const desc = item.description || 'No description';
            const source = item.source || '';
            const findings = item.key_findings || '';

            let card = '<div class="research-card">';
            card += '<div class="research-header">';
            card += '<h3>' + title + '</h3>';
            card += '<span class="research-badge">' + type + '</span>';
            card += '</div>';
            card += '<div class="research-body">';
            card += '<div class="field"><strong>Method:</strong> ' + method + '</div>';
            card += '<div class="field"><strong>Description:</strong> ' + desc + '</div>';
            if (source) card += '<div class="field"><strong>Source:</strong> ' + source + '</div>';
            if (findings) card += '<div class="field"><strong>Key Findings:</strong> ' + findings + '</div>';
            card += '</div>';
            card += '<div class="research-footer admin-only">';
            card += '<button class="btn-secondary btn-sm" onclick="capstoneHub.editResearchItem(' + item.id + ')"><i class="fas fa-edit"></i> Edit</button>';
            card += '<button class="btn-danger btn-sm" onclick="capstoneHub.deleteResearchItem(' + item.id + ')"><i class="fas fa-trash"></i> Delete</button>';
            card += '</div></div>';
            return card;
        }).join('');
    }

// 4. INTEGRATIONS RENDER (replace line 362-370)
    renderIntegrations() {
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
        }).join('');
    }
