// Enhanced Capstone Hub - JavaScript Application Logic

class CapstoneHub {
    constructor() {
        this.currentSection = 'dashboard';
        this.data = {
            deliverables: [],
            processes: [],
            aiTechnologies: [],
            softwareTools: [],
            researchItems: [],
            integrations: []
        };
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupEventListeners();
        this.loadInitialData();
        this.updateDashboard();
    }

    // Navigation Management
    setupNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.navigateToSection(section);
            });
        });
    }

    navigateToSection(section) {
        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Show/hide content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        this.currentSection = section;
        this.loadSectionData(section);
    }

    // Event Listeners
    setupEventListeners() {
        // Tab buttons for AI Technologies
        document.querySelectorAll('.ai-categories .tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.ai-categories .tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.filterAITechnologies(btn.getAttribute('data-category'));
            });
        });

        // Tab buttons for Research
        document.querySelectorAll('.research-tabs .tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.research-tabs .tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.filterResearch(btn.getAttribute('data-type'));
            });
        });

        // Filter listeners
        document.getElementById('phase-filter')?.addEventListener('change', () => this.filterDeliverables());
        document.getElementById('status-filter')?.addEventListener('change', () => this.filterDeliverables());
        document.getElementById('process-search')?.addEventListener('input', () => this.filterProcesses());
        document.getElementById('department-filter')?.addEventListener('change', () => this.filterProcesses());
        document.getElementById('automation-filter')?.addEventListener('change', () => this.filterProcesses());
    }

    // Data Loading
    async loadInitialData() {
        try {
            // Load data from API endpoints
            await Promise.all([
                this.loadDeliverables(),
                this.loadProcesses(),
                this.loadAITechnologies(),
                this.loadSoftwareTools(),
                this.loadResearchItems(),
                this.loadIntegrations()
            ]);
            this.updateDashboard();
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    async loadDeliverables() {
        try {
            console.log('[DEBUG] Fetching deliverables from /api/deliverables');
            const response = await fetch('/api/deliverables');
            console.log('[DEBUG] Deliverables response status:', response.status, response.statusText);
            if (response.ok) {
                this.data.deliverables = await response.json();
                console.log('[DEBUG] Loaded deliverables:', this.data.deliverables.length, 'items');
                this.renderDeliverables();
            } else {
                const errorText = await response.text();
                console.error('[ERROR] Failed to load deliverables:', response.status, errorText);
                this.showEmptyState('deliverables-timeline', 'deliverables', 'Failed to load deliverables', 'Check console for errors');
            }
        } catch (error) {
            console.error('[ERROR] Error loading deliverables:', error);
            this.showEmptyState('deliverables-timeline', 'deliverables', 'No deliverables yet', 'Add your first deliverable to get started');
        }
    }

    async loadProcesses() {
        try {
            console.log('[DEBUG] Fetching business processes from /api/business-processes');
            const response = await fetch('/api/business-processes');
            console.log('[DEBUG] Business processes response status:', response.status, response.statusText);
            if (response.ok) {
                this.data.processes = await response.json();
                console.log('[DEBUG] Loaded business processes:', this.data.processes.length, 'items');
                this.renderProcesses();
            } else {
                const errorText = await response.text();
                console.error('[ERROR] Failed to load business processes:', response.status, errorText);
                this.showEmptyState('processes-grid', 'sitemap', 'Failed to load processes', 'Check console for errors');
            }
        } catch (error) {
            console.error('[ERROR] Error loading processes:', error);
            this.showEmptyState('processes-grid', 'sitemap', 'No business processes yet', 'Add your first process to begin evaluation');
        }
    }

    async loadAITechnologies() {
        try {
            const response = await fetch('/api/ai-technologies');
            if (response.ok) {
                this.data.aiTechnologies = await response.json();
                this.renderAITechnologies();
            }
        } catch (error) {
            console.error('Error loading AI technologies:', error);
            this.showEmptyState('ai-tech-grid', 'robot', 'No AI technologies yet', 'Add your first AI technology to start building your catalog');
        }
    }

    async loadSoftwareTools() {
        try {
            const response = await fetch('/api/software-tools');
            if (response.ok) {
                this.data.softwareTools = await response.json();
                this.renderSoftwareTools();
            }
        } catch (error) {
            console.error('Error loading software tools:', error);
            this.showEmptyState('core-tools', 'tools', 'No core tools yet', 'Add your first software tool');
            this.showEmptyState('optional-tools', 'tools', 'No optional tools yet', 'Add optional tools for evaluation');
            this.showEmptyState('integration-tools', 'tools', 'No integration tools yet', 'Add integration tools');
        }
    }

    async loadResearchItems() {
        try {
            console.log('[DEBUG] Fetching research items from /api/research-items');
            const response = await fetch('/api/research-items');
            console.log('[DEBUG] Research items response status:', response.status, response.statusText);
            if (response.ok) {
                this.data.researchItems = await response.json();
                console.log('[DEBUG] Loaded research items:', this.data.researchItems.length, 'items');
                this.renderResearchItems();
            } else {
                const errorText = await response.text();
                console.error('[ERROR] Failed to load research items:', response.status, errorText);
                this.showEmptyState('research-content', 'search', 'Failed to load research items', 'Check console for errors');
            }
        } catch (error) {
            console.error('[ERROR] Error loading research items:', error);
            this.showEmptyState('research-content', 'search', 'No research items yet', 'Add your first research item to begin documentation');
        }
    }

    async loadIntegrations() {
        try {
            const response = await fetch('/api/integrations');
            if (response.ok) {
                this.data.integrations = await response.json();
                this.renderIntegrations();
            }
        } catch (error) {
            console.error('Error loading integrations:', error);
            this.showEmptyState('integration-logs', 'plug', 'No integration logs yet', 'Configure your first integration');
        }
    }

    loadSectionData(section) {
        switch (section) {
            case 'deliverables':
                this.loadDeliverables();
                break;
            case 'processes':
                this.loadProcesses();
                break;
            case 'ai-technologies':
                this.loadAITechnologies();
                break;
            case 'software-tools':
                this.loadSoftwareTools();
                break;
            case 'research':
                this.loadResearchItems();
                break;
            case 'integrations':
                this.loadIntegrations();
                break;
        }
    }

    // Dashboard Updates
    updateDashboard() {
        document.getElementById('deliverables-count').textContent = this.data.deliverables.length;
        document.getElementById('processes-count').textContent = this.data.processes.length;
        document.getElementById('ai-tech-count').textContent = this.data.aiTechnologies.length;
        document.getElementById('research-count').textContent = this.data.researchItems.length;

        this.updateCharts();
        this.updateRecentActivity();
    }

    updateCharts() {
        // Placeholder for chart updates
        const deliverablesChart = document.getElementById('deliverables-chart');
        const processesChart = document.getElementById('processes-chart');
        
        if (deliverablesChart && this.data.deliverables.length === 0) {
            deliverablesChart.parentElement.innerHTML = '<div class="empty-state"><i class="fas fa-chart-bar"></i><p>Charts will appear when you add deliverables</p></div>';
        }
        
        if (processesChart && this.data.processes.length === 0) {
            processesChart.parentElement.innerHTML = '<div class="empty-state"><i class="fas fa-chart-pie"></i><p>Charts will appear when you add processes</p></div>';
        }
    }

    updateRecentActivity() {
        const activityList = document.getElementById('recent-activity');
        if (activityList) {
            if (this.getAllItems().length === 0) {
                activityList.innerHTML = '<div class="empty-state"><i class="fas fa-clock"></i><p>Recent activity will appear here</p></div>';
            } else {
                activityList.innerHTML = '<div class="empty-state"><i class="fas fa-clock"></i><p>Activity tracking coming soon</p></div>';
            }
        }
    }

    getAllItems() {
        return [
            ...this.data.deliverables,
            ...this.data.processes,
            ...this.data.aiTechnologies,
            ...this.data.softwareTools,
            ...this.data.researchItems,
            ...this.data.integrations
        ];
    }

    // Rendering Methods
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

    renderProcesses() {
        const container = document.getElementById('processes-grid');
        if (this.data.processes.length === 0) {
            this.showEmptyState('processes-grid', 'sitemap', 'No business processes yet', 'Add your first process to begin evaluation and optimization');
            return;
        }
        
        container.innerHTML = this.data.processes.map(process => {
            const name = process.name || 'Untitled Process';
            const dept = process.department || 'Not specified';
            const automation = process.automation_potential || 'Not Set';
            const desc = process.description || 'No description provided';
            const currentState = process.current_state || 'Not documented';
            const painPoints = process.pain_points || '';
            const aiRec = process.ai_recommendations || '';
            const priority = process.priority_score || '';
            
            let card = '<div class="process-card">';
            card += '<div class="process-header">';
            card += '<h3>' + name + '</h3>';
            card += '<span class="process-badge">' + automation + '</span>';
            card += '</div>';
            card += '<div class="process-body">';
            card += '<div class="process-field"><strong>Department:</strong> ' + dept + '</div>';
            card += '<div class="process-field"><strong>Description:</strong> ' + desc + '</div>';
            card += '<div class="process-field"><strong>Current State:</strong> ' + currentState + '</div>';
            if (painPoints) card += '<div class="process-field"><strong>Pain Points:</strong> ' + painPoints + '</div>';
            if (aiRec) card += '<div class="process-field"><strong>AI Recommendations:</strong> ' + aiRec + '</div>';
            if (priority) card += '<div class="process-field"><strong>Priority Score:</strong> ' + priority + '/10</div>';
            card += '</div>';
            card += '<div class="process-footer admin-only">';
            card += '<button class="btn-secondary btn-sm" onclick="capstoneHub.editProcess(' + process.id + ')"><i class="fas fa-edit"></i> Edit</button>';
            card += '<button class="btn-danger btn-sm" onclick="capstoneHub.deleteProcess(' + process.id + ')"><i class="fas fa-trash"></i> Delete</button>';
            card += '</div>';
            card += '</div>';
            return card;
        }).join('');
    }

