#!/bin/bash
cd src/static

# Replace renderDeliverables (lines 271-279)
sed -i '271,279c\
    renderDeliverables() {\
        const container = document.getElementById('"'"'deliverables-timeline'"'"');\
        if (this.data.deliverables.length === 0) {\
            this.showEmptyState('"'"'deliverables-timeline'"'"', '"'"'tasks'"'"', '"'"'No deliverables yet'"'"', '"'"'Add your first deliverable to get started with timeline tracking'"'"');\
            return;\
        }\
        container.innerHTML = this.data.deliverables.map(item => { const title = item.title || '"'"'Untitled'"'"'; const desc = item.description || '"'"''"'"'; const dueDate = item.due_date || '"'"'No date'"'"'; const phase = item.phase || '"'"'Unassigned'"'"'; const status = item.status || '"'"'Not started'"'"'; let card = '"'"'<div class="deliverable-card"><div class="deliverable-header"><h3>'"'"' + title + '"'"'</h3><span class="status-badge">'"'"' + status + '"'"'</span></div><div class="deliverable-body"><div class="field"><strong>Phase:</strong> '"'"' + phase + '"'"'</div><div class="field"><strong>Due Date:</strong> '"'"' + dueDate + '"'"'</div>'"'"' + (desc ? '"'"'<div class="field"><strong>Description:</strong> '"'"' + desc + '"'"'</div>'"'"' : '"'"''"'"') + '"'"'</div><div class="deliverable-footer admin-only"><button class="btn-secondary btn-sm" onclick="capstoneHub.editDeliverable('"'"' + item.id + '"'"')"><i class="fas fa-edit"></i> Edit</button><button class="btn-danger btn-sm" onclick="capstoneHub.deleteDeliverable('"'"' + item.id + '"'"')"><i class="fas fa-trash"></i> Delete</button></div></div>'"'"'; return card; }).join('"'"''"'"');\
    }' app.js

echo "Done - 1 of 3 functions replaced"

# Replace renderAITechnologies (lines 320-328)
sed -i '320,328c\
    renderAITechnologies() {\
        const container = document.getElementById('"'"'ai-tech-grid'"'"');\
        if (this.data.aiTechnologies.length === 0) {\
            this.showEmptyState('"'"'ai-tech-grid'"'"', '"'"'robot'"'"', '"'"'No AI technologies yet'"'"', '"'"'Add your first AI technology to start building your comprehensive catalog'"'"');\
            return;\
        }\
        container.innerHTML = this.data.aiTechnologies.map(tech => { const name = tech.name || '"'"'Untitled'"'"'; const category = tech.category || '"'"'Uncategorized'"'"'; const desc = tech.description || '"'"'No description'"'"'; const useCase = tech.use_case || '"'"''"'"'; const maturity = tech.maturity_level || '"'"'Unknown'"'"'; let card = '"'"'<div class="tech-card"><div class="tech-header"><h3>'"'"' + name + '"'"'</h3><span class="tech-badge">'"'"' + category + '"'"'</span></div><div class="tech-body"><div class="field"><strong>Maturity:</strong> '"'"' + maturity + '"'"'</div><div class="field"><strong>Description:</strong> '"'"' + desc + '"'"'</div>'"'"' + (useCase ? '"'"'<div class="field"><strong>Use Case:</strong> '"'"' + useCase + '"'"'</div>'"'"' : '"'"''"'"') + '"'"'</div><div class="tech-footer admin-only"><button class="btn-secondary btn-sm" onclick="capstoneHub.editAITechnology('"'"' + tech.id + '"'"')"><i class="fas fa-edit"></i> Edit</button><button class="btn-danger btn-sm" onclick="capstoneHub.deleteAITechnology('"'"' + tech.id + '"'"')"><i class="fas fa-trash"></i> Delete</button></div></div>'"'"'; return card; }).join('"'"''"'"');\
    }' app.js

echo "Done - 2 of 3 functions replaced"

# Replace renderIntegrations (lines 362-370)
sed -i '362,370c\
    renderIntegrations() {\
        const container = document.getElementById('"'"'integration-logs'"'"');\
        if (this.data.integrations.length === 0) {\
            this.showEmptyState('"'"'integration-logs'"'"', '"'"'plug'"'"', '"'"'No integration activity yet'"'"', '"'"'Configure your first integration to see activity logs'"'"');\
            return;\
        }\
        container.innerHTML = this.data.integrations.map(item => { const name = item.name || '"'"'Untitled Integration'"'"'; const type = item.integration_type || '"'"'Unknown'"'"'; const status = item.status || '"'"'Inactive'"'"'; const desc = item.description || '"'"'No description'"'"'; const endpoint = item.api_endpoint || '"'"''"'"'; let card = '"'"'<div class="integration-card"><div class="integration-header"><h3>'"'"' + name + '"'"'</h3><span class="status-badge status-'"'"' + status.toLowerCase() + '"'"'">'"'"' + status + '"'"'</span></div><div class="integration-body"><div class="field"><strong>Type:</strong> '"'"' + type + '"'"'</div><div class="field"><strong>Description:</strong> '"'"' + desc + '"'"'</div>'"'"' + (endpoint ? '"'"'<div class="field"><strong>Endpoint:</strong> '"'"' + endpoint + '"'"'</div>'"'"' : '"'"''"'"') + '"'"'</div><div class="integration-footer admin-only"><button class="btn-secondary btn-sm" onclick="capstoneHub.editIntegration('"'"' + item.id + '"'"')"><i class="fas fa-edit"></i> Edit</button><button class="btn-danger btn-sm" onclick="capstoneHub.deleteIntegration('"'"' + item.id + '"'"')"><i class="fas fa-trash"></i> Delete</button></div></div>'"'"'; return card; }).join('"'"''"'"');\
    }' app.js

echo "Done - All 3 functions replaced!"
echo "Verifying..."
grep -c "Loading deliverables\|Loading AI technologies\|Loading integration logs" app.js
