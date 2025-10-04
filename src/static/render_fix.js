    renderProcesses() {
        const container = document.getElementById('processes-grid');
        if (this.data.processes.length === 0) {
            this.showEmptyState('processes-grid', 'sitemap', 'No business processes yet', 'Add your first process to begin evaluation and optimization');
            return;
        }
        
        // Actually render the processes
        container.innerHTML = this.data.processes.map(process => `
            <div class="process-card">
                <div class="process-header">
                    <h3>${process.name || 'Untitled Process'}</h3>
                    <span class="process-badge ${(process.automation_potential || '').toLowerCase().replace(/\s+/g, '-')}">${process.automation_potential || 'Not Set'}</span>
                </div>
                <div class="process-body">
                    <div class="process-field">
                        <strong>Department:</strong> ${process.department || 'Not specified'}
                    </div>
                    <div class="process-field">
                        <strong>Description:</strong> ${process.description || 'No description provided'}
                    </div>
                    <div class="process-field">
                        <strong>Current State:</strong> ${process.current_state || 'Not documented'}
                    </div>
                    ${process.pain_points ? `<div class="process-field"><strong>Pain Points:</strong> ${process.pain_points}</div>` : ''}
                    ${process.ai_recommendations ? `<div class="process-field"><strong>AI Recommendations:</strong> ${process.ai_recommendations}</div>` : ''}
                    ${process.priority_score ? `<div class="process-field"><strong>Priority Score:</strong> ${process.priority_score}/10</div>` : ''}
                </div>
                <div class="process-footer admin-only">
                    <button class="btn-secondary btn-sm" onclick="capstoneHub.editProcess(${process.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-danger btn-sm" onclick="capstoneHub.deleteProcess(${process.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `).join('');
    }
