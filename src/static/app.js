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
            const response = await fetch('/api/deliverables');
            if (response.ok) {
                this.data.deliverables = await response.json();
                this.renderDeliverables();
            }
        } catch (error) {
            console.error('Error loading deliverables:', error);
            this.showEmptyState('deliverables-timeline', 'deliverables', 'No deliverables yet', 'Add your first deliverable to get started');
        }
    }

    async loadProcesses() {
        try {
            const response = await fetch('/api/business-processes');
            if (response.ok) {
                this.data.processes = await response.json();
                this.renderProcesses();
            }
        } catch (error) {
            console.error('Error loading processes:', error);
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
            const response = await fetch('/api/research-items');
            if (response.ok) {
                this.data.researchItems = await response.json();
                this.renderResearchItems();
            }
        } catch (error) {
            console.error('Error loading research items:', error);
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
        // Render deliverables timeline here
        container.innerHTML = '<div class="loading">Loading deliverables...</div>';
    }

    renderProcesses() {
        const container = document.getElementById('processes-grid');
        if (this.data.processes.length === 0) {
            this.showEmptyState('processes-grid', 'sitemap', 'No business processes yet', 'Add your first process to begin evaluation and optimization');
            return;
        }
        // Render processes grid here
        container.innerHTML = '<div class="loading">Loading processes...</div>';
    }

    renderAITechnologies() {
        const container = document.getElementById('ai-tech-grid');
        if (this.data.aiTechnologies.length === 0) {
            this.showEmptyState('ai-tech-grid', 'robot', 'No AI technologies yet', 'Add your first AI technology to start building your comprehensive catalog');
            return;
        }
        // Render AI technologies grid here
        container.innerHTML = '<div class="loading">Loading AI technologies...</div>';
    }

    renderSoftwareTools() {
        const coreTools = document.getElementById('core-tools');
        const optionalTools = document.getElementById('optional-tools');
        const integrationTools = document.getElementById('integration-tools');

        if (this.data.softwareTools.length === 0) {
            this.showEmptyState('core-tools', 'tools', 'No core tools yet', 'Add essential software tools');
            this.showEmptyState('optional-tools', 'tools', 'No optional tools yet', 'Add tools for evaluation');
            this.showEmptyState('integration-tools', 'tools', 'No integration tools yet', 'Add integration solutions');
            return;
        }

        // Filter and render by tool type
        const core = this.data.softwareTools.filter(tool => tool.tool_type === 'Core');
        const optional = this.data.softwareTools.filter(tool => tool.tool_type === 'Optional');
        const integration = this.data.softwareTools.filter(tool => tool.tool_type === 'Integration');

        coreTools.innerHTML = core.length ? '<div class="loading">Loading core tools...</div>' : '<div class="empty-state"><i class="fas fa-tools"></i><p>No core tools yet</p></div>';
        optionalTools.innerHTML = optional.length ? '<div class="loading">Loading optional tools...</div>' : '<div class="empty-state"><i class="fas fa-tools"></i><p>No optional tools yet</p></div>';
        integrationTools.innerHTML = integration.length ? '<div class="loading">Loading integration tools...</div>' : '<div class="empty-state"><i class="fas fa-tools"></i><p>No integration tools yet</p></div>';
    }

    renderResearchItems() {
        const container = document.getElementById('research-content');
        if (this.data.researchItems.length === 0) {
            this.showEmptyState('research-content', 'search', 'No research items yet', 'Add your first research item to begin comprehensive documentation and tracking');
            return;
        }
        // Render research items here
        container.innerHTML = '<div class="loading">Loading research items...</div>';
    }

    renderIntegrations() {
        const container = document.getElementById('integration-logs');
        if (this.data.integrations.length === 0) {
            this.showEmptyState('integration-logs', 'plug', 'No integration activity yet', 'Configure your first integration to see activity logs');
            return;
        }
        // Render integration logs here
        container.innerHTML = '<div class="loading">Loading integration logs...</div>';
    }

    // Filtering Methods
    filterDeliverables() {
        const phaseFilter = document.getElementById('phase-filter').value;
        const statusFilter = document.getElementById('status-filter').value;
        // Apply filters and re-render
        this.renderDeliverables();
    }

    filterProcesses() {
        const searchTerm = document.getElementById('process-search').value.toLowerCase();
        const departmentFilter = document.getElementById('department-filter').value;
        const automationFilter = document.getElementById('automation-filter').value;
        // Apply filters and re-render
        this.renderProcesses();
    }

    filterAITechnologies(category) {
        // Filter AI technologies by category and re-render
        this.renderAITechnologies();
    }

    filterResearch(type) {
        // Filter research items by type and re-render
        this.renderResearchItems();
    }

    // Modal Management
    showModal(title, content) {
        const modal = document.getElementById('modal-overlay');
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');

        modalTitle.textContent = title;
        modalBody.innerHTML = content;
        modal.classList.add('active');
    }

    closeModal() {
        const modal = document.getElementById('modal-overlay');
        modal.classList.remove('active');
    }

    // Empty State Helper
    showEmptyState(containerId, icon, title, description) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-${icon}"></i>
                    <h3>${title}</h3>
                    <p>${description}</p>
                </div>
            `;
        }
    }

    // Add Item Methods (Modal Forms)
    addDeliverable() {
        const form = `
            <form id="deliverable-form">
                <div class="form-group mb-3">
                    <label for="deliverable-title">Title</label>
                    <input type="text" id="deliverable-title" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="deliverable-description">Description</label>
                    <textarea id="deliverable-description" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-group mb-3">
                    <label for="deliverable-phase">Phase</label>
                    <select id="deliverable-phase" class="form-control" required>
                        <option value="">Select Phase</option>
                        <option value="Foundation">Foundation & Planning</option>
                        <option value="Research">Research & Analysis</option>
                        <option value="Implementation">Implementation</option>
                        <option value="Evaluation">Evaluation & Testing</option>
                        <option value="Final">Final Report & Presentation</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="deliverable-due-date">Due Date</label>
                    <input type="date" id="deliverable-due-date" class="form-control">
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add Deliverable</button>
                </div>
            </form>
        `;
        this.showModal('Add Deliverable', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('deliverable-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveDeliverable();
                });
            }
        }, 100);
    }

    async saveDeliverable() {
        const title = document.getElementById('deliverable-title').value;
        const description = document.getElementById('deliverable-description').value;
        const phase = document.getElementById('deliverable-phase').value;
        const dueDate = document.getElementById('deliverable-due-date').value;

        try {
            const response = await fetch('/api/deliverables', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    phase: phase,
                    due_date: dueDate
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.deliverables.push(newItem);
                this.closeModal();
                this.loadDeliverables();
                this.updateDashboard();
                showNotification('Deliverable added successfully!', 'success');
            } else {
                showNotification('Error adding deliverable', 'error');
            }
        } catch (error) {
            console.error('Error saving deliverable:', error);
            showNotification('Error adding deliverable', 'error');
        }
    }

    addProcess() {
        const form = `
            <form id="process-form">
                <div class="form-group mb-3">
                    <label for="process-name">Process Name</label>
                    <input type="text" id="process-name" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="process-department">Department</label>
                    <select id="process-department" class="form-control" required>
                        <option value="">Select Department</option>
                        <option value="Sales">Sales</option>
                        <option value="Operations">Operations</option>
                        <option value="Customer Service">Customer Service</option>
                        <option value="Finance">Finance</option>
                        <option value="IT">IT</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="process-description">Description</label>
                    <textarea id="process-description" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-group mb-3">
                    <label for="process-automation">Automation Potential</label>
                    <select id="process-automation" class="form-control">
                        <option value="">Select Potential</option>
                        <option value="High">High</option>
                        <option value="Medium">Medium</option>
                        <option value="Low">Low</option>
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add Process</button>
                </div>
            </form>
        `;
        this.showModal('Add Business Process', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('process-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveProcess();
                });
            }
        }, 100);
    }

    async saveProcess() {
        const name = document.getElementById('process-name').value;
        const department = document.getElementById('process-department').value;
        const description = document.getElementById('process-description').value;
        const automationPotential = document.getElementById('process-automation').value;

        try {
            const response = await fetch('/api/business-processes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    department: department,
                    description: description,
                    automation_potential: automationPotential
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.processes.push(newItem);
                this.closeModal();
                this.loadProcesses();
                this.updateDashboard();
                showNotification('Business process added successfully!', 'success');
            } else {
                showNotification('Error adding business process', 'error');
            }
        } catch (error) {
            console.error('Error saving business process:', error);
            showNotification('Error adding business process', 'error');
        }
    }

    addAITechnology() {
        const form = `
            <form id="ai-tech-form">
                <div class="form-group mb-3">
                    <label for="ai-tech-name">Technology Name</label>
                    <input type="text" id="ai-tech-name" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="ai-tech-category">Category</label>
                    <select id="ai-tech-category" class="form-control" required>
                        <option value="">Select Category</option>
                        <option value="Generative">Generative AI</option>
                        <option value="Agentic">Agentic AI</option>
                        <option value="Embedded">Embedded AI</option>
                        <option value="Predictive">Predictive AI</option>
                        <option value="Computer Vision">Computer Vision</option>
                        <option value="NLP">Natural Language Processing</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="ai-tech-provider">Platform Provider</label>
                    <input type="text" id="ai-tech-provider" class="form-control" placeholder="e.g., OpenAI, Microsoft, Google">
                </div>
                <div class="form-group mb-3">
                    <label for="ai-tech-description">Description</label>
                    <textarea id="ai-tech-description" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add AI Technology</button>
                </div>
            </form>
        `;
        this.showModal('Add AI Technology', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('ai-tech-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveAITechnology();
                });
            }
        }, 100);
    }

    async saveAITechnology() {
        const name = document.getElementById('ai-tech-name').value;
        const category = document.getElementById('ai-tech-category').value;
        const provider = document.getElementById('ai-tech-provider').value;
        const description = document.getElementById('ai-tech-description').value;

        try {
            const response = await fetch('/api/ai-technologies', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    category: category,
                    provider: provider,
                    description: description
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.aiTechnologies.push(newItem);
                this.closeModal();
                this.loadAITechnologies();
                this.updateDashboard();
                showNotification('AI technology added successfully!', 'success');
            } else {
                showNotification('Error adding AI technology', 'error');
            }
        } catch (error) {
            console.error('Error saving AI technology:', error);
            showNotification('Error adding AI technology', 'error');
        }
    }

    addSoftwareTool() {
        const form = `
            <form id="software-tool-form">
                <div class="form-group mb-3">
                    <label for="tool-name">Tool Name</label>
                    <input type="text" id="tool-name" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="tool-category">Category</label>
                    <select id="tool-category" class="form-control" required>
                        <option value="">Select Category</option>
                        <option value="CRM">CRM</option>
                        <option value="ERP">ERP</option>
                        <option value="Cloud">Cloud Platform</option>
                        <option value="Analytics">Analytics</option>
                        <option value="Communication">Communication</option>
                        <option value="Project Management">Project Management</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="tool-type">Tool Type</label>
                    <select id="tool-type" class="form-control" required>
                        <option value="">Select Type</option>
                        <option value="Core">Core</option>
                        <option value="Optional">Optional</option>
                        <option value="Integration">Integration</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="tool-description">Description</label>
                    <textarea id="tool-description" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add Software Tool</button>
                </div>
            </form>
        `;
        this.showModal('Add Software Tool', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('software-tool-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveSoftwareTool();
                });
            }
        }, 100);
    }

    async saveSoftwareTool() {
        const name = document.getElementById('tool-name').value;
        const category = document.getElementById('tool-category').value;
        const toolType = document.getElementById('tool-type').value;
        const description = document.getElementById('tool-description').value;

        try {
            const response = await fetch('/api/software-tools', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    category: category,
                    tool_type: toolType,
                    description: description
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.softwareTools.push(newItem);
                this.closeModal();
                this.loadSoftwareTools();
                this.updateDashboard();
                showNotification('Software tool added successfully!', 'success');
            } else {
                showNotification('Error adding software tool', 'error');
            }
        } catch (error) {
            console.error('Error saving software tool:', error);
            showNotification('Error adding software tool', 'error');
        }
    }

    addResearchItem() {
        const form = `
            <form id="research-form">
                <div class="form-group mb-3">
                    <label for="research-title">Research Title</label>
                    <input type="text" id="research-title" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="research-type">Research Type</label>
                    <select id="research-type" class="form-control" required>
                        <option value="">Select Type</option>
                        <option value="Primary">Primary Research</option>
                        <option value="Secondary">Secondary Research</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="research-method">Research Method</label>
                    <select id="research-method" class="form-control">
                        <option value="">Select Method</option>
                        <option value="Interview">Interview</option>
                        <option value="Survey">Survey</option>
                        <option value="Literature Review">Literature Review</option>
                        <option value="Case Study">Case Study</option>
                        <option value="Observation">Observation</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="research-description">Description</label>
                    <textarea id="research-description" class="form-control" rows="3"></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add Research Item</button>
                </div>
            </form>
        `;
        this.showModal('Add Research Item', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('research-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveResearchItem();
                });
            }
        }, 100);
    }

    async saveResearchItem() {
        const title = document.getElementById('research-title').value;
        const researchType = document.getElementById('research-type').value;
        const researchMethod = document.getElementById('research-method').value;
        const description = document.getElementById('research-description').value;

        try {
            const response = await fetch('/api/research-items', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    research_type: researchType,
                    research_method: researchMethod,
                    description: description
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.researchItems.push(newItem);
                this.closeModal();
                this.loadResearchItems();
                this.updateDashboard();
                showNotification('Research item added successfully!', 'success');
            } else {
                showNotification('Error adding research item', 'error');
            }
        } catch (error) {
            console.error('Error saving research item:', error);
            showNotification('Error adding research item', 'error');
        }
    }

    addIntegration() {
        const form = `
            <form id="integration-form">
                <div class="form-group mb-3">
                    <label for="integration-name">Integration Name</label>
                    <input type="text" id="integration-name" class="form-control" required>
                </div>
                <div class="form-group mb-3">
                    <label for="integration-platform">Platform</label>
                    <select id="integration-platform" class="form-control" required>
                        <option value="">Select Platform</option>
                        <option value="Notion">Notion</option>
                        <option value="Microsoft">Microsoft 365</option>
                        <option value="Google">Google Workspace</option>
                        <option value="Salesforce">Salesforce</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="integration-type">Integration Type</label>
                    <select id="integration-type" class="form-control">
                        <option value="">Select Type</option>
                        <option value="API">API</option>
                        <option value="Webhook">Webhook</option>
                        <option value="Export/Import">Export/Import</option>
                        <option value="Direct Connection">Direct Connection</option>
                    </select>
                </div>
                <div class="form-group mb-3">
                    <label for="integration-purpose">Purpose</label>
                    <textarea id="integration-purpose" class="form-control" rows="3" placeholder="What will this integration accomplish?"></textarea>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Add Integration</button>
                </div>
            </form>
        `;
        this.showModal('Add Integration', form);

        // Add form submit handler
        setTimeout(() => {
            const formElement = document.getElementById('integration-form');
            if (formElement) {
                formElement.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    await this.saveIntegration();
                });
            }
        }, 100);
    }

    async saveIntegration() {
        const name = document.getElementById('integration-name').value;
        const platform = document.getElementById('integration-platform').value;
        const integrationType = document.getElementById('integration-type').value;
        const purpose = document.getElementById('integration-purpose').value;

        try {
            const response = await fetch('/api/integrations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    platform: platform,
                    integration_type: integrationType,
                    purpose: purpose
                })
            });

            if (response.ok) {
                const newItem = await response.json();
                this.data.integrations.push(newItem);
                this.closeModal();
                this.loadIntegrations();
                this.updateDashboard();
                showNotification('Integration added successfully!', 'success');
            } else {
                showNotification('Error adding integration', 'error');
            }
        } catch (error) {
            console.error('Error saving integration:', error);
            showNotification('Error adding integration', 'error');
        }
    }
}

// Global Functions (for onclick handlers)
function addDeliverable() {
    capstoneHub.addDeliverable();
}

function addProcess() {
    capstoneHub.addProcess();
}

function addAITechnology() {
    capstoneHub.addAITechnology();
}

function addSoftwareTool() {
    capstoneHub.addSoftwareTool();
}

function addResearchItem() {
    capstoneHub.addResearchItem();
}

function addIntegration() {
    capstoneHub.addIntegration();
}

function closeModal() {
    capstoneHub.closeModal();
}

// Initialize the application
let capstoneHub;
document.addEventListener('DOMContentLoaded', () => {
    capstoneHub = new CapstoneHub();
});

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        closeModal();
    }
});

// Handle escape key for modal
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});

// Add some CSS for form styling
const formStyles = `
<style>
.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--gray-700);
}

.form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--gray-300);
    border-radius: var(--border-radius);
    font-size: 0.875rem;
    transition: border-color 0.2s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--gray-200);
}
</style>
`;

// Inject form styles
document.head.insertAdjacentHTML('beforeend', formStyles);

// ============================================
// DROPDOWN OPTIONS MANAGEMENT
// ============================================

// Default dropdown options
const defaultDropdownOptions = {
    departments: ['Sales', 'Operations', 'Customer Service', 'Finance', 'IT'],
    automationPotential: ['High', 'Medium', 'Low']
};

// Load dropdown options from localStorage or use defaults
function getDropdownOptions() {
    const stored = localStorage.getItem('processDropdownOptions');
    if (stored) {
        return JSON.parse(stored);
    }
    return { ...defaultDropdownOptions };
}

// Save dropdown options to localStorage
function saveDropdownOptions(options) {
    localStorage.setItem('processDropdownOptions', JSON.stringify(options));
}

// Function to edit process dropdowns
function editProcessDropdowns() {
    const options = getDropdownOptions();

    const form = `
        <form id="dropdown-options-form">
            <div class="dropdown-editor-section">
                <h3 style="margin-bottom: 1rem; color: var(--gray-700);">Departments</h3>
                <div id="departments-list" class="options-list">
                    ${options.departments.map((dept, index) => `
                        <div class="option-item">
                            <input type="text" value="${dept}" class="form-control" data-type="department" data-index="${index}">
                            <button type="button" class="btn-danger-sm" onclick="removeOption('department', ${index})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
                <button type="button" class="btn-secondary-sm" onclick="addOption('department')">
                    <i class="fas fa-plus"></i> Add Department
                </button>
            </div>

            <div class="dropdown-editor-section" style="margin-top: 2rem;">
                <h3 style="margin-bottom: 1rem; color: var(--gray-700);">Automation Potential</h3>
                <div id="automation-list" class="options-list">
                    ${options.automationPotential.map((auto, index) => `
                        <div class="option-item">
                            <input type="text" value="${auto}" class="form-control" data-type="automation" data-index="${index}">
                            <button type="button" class="btn-danger-sm" onclick="removeOption('automation', ${index})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
                <button type="button" class="btn-secondary-sm" onclick="addOption('automation')">
                    <i class="fas fa-plus"></i> Add Option
                </button>
            </div>

            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                <button type="button" class="btn-secondary" onclick="resetDropdownOptions()">Reset to Defaults</button>
                <button type="submit" class="btn-primary">Save Changes</button>
            </div>
        </form>

        <style>
        .dropdown-editor-section {
            margin-bottom: 1.5rem;
        }
        .options-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        .option-item {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .option-item input {
            flex: 1;
        }
        .btn-danger-sm, .btn-secondary-sm {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-danger-sm {
            background-color: var(--error-color);
            color: white;
        }
        .btn-danger-sm:hover {
            background-color: #dc2626;
        }
        .btn-secondary-sm {
            background-color: var(--gray-200);
            color: var(--gray-700);
        }
        .btn-secondary-sm:hover {
            background-color: var(--gray-300);
        }
        </style>
    `;

    capstoneHub.showModal('Edit Dropdown Options', form);

    // Add form submit handler
    setTimeout(() => {
        document.getElementById('dropdown-options-form').addEventListener('submit', function(e) {
            e.preventDefault();
            saveDropdownChanges();
        });
    }, 100);
}

// Add new option to list
function addOption(type) {
    const listId = type === 'department' ? 'departments-list' : 'automation-list';
    const list = document.getElementById(listId);
    const currentCount = list.querySelectorAll('.option-item').length;

    const newItem = document.createElement('div');
    newItem.className = 'option-item';
    newItem.innerHTML = `
        <input type="text" value="" class="form-control" data-type="${type}" data-index="${currentCount}" placeholder="Enter new ${type === 'department' ? 'department' : 'option'}">
        <button type="button" class="btn-danger-sm" onclick="removeOption('${type}', ${currentCount})">
            <i class="fas fa-trash"></i>
        </button>
    `;
    list.appendChild(newItem);
}

// Remove option from list
function removeOption(type, index) {
    const listId = type === 'department' ? 'departments-list' : 'automation-list';
    const list = document.getElementById(listId);
    const items = list.querySelectorAll('.option-item');

    if (items.length > 1) {
        items[index].remove();
        // Re-index remaining items
        const remainingItems = list.querySelectorAll('.option-item');
        remainingItems.forEach((item, newIndex) => {
            const input = item.querySelector('input');
            const button = item.querySelector('button');
            input.setAttribute('data-index', newIndex);
            button.setAttribute('onclick', `removeOption('${type}', ${newIndex})`);
        });
    } else {
        alert('You must have at least one option.');
    }
}

// Save dropdown changes
function saveDropdownChanges() {
    const departments = [];
    const automation = [];

    // Collect department options
    document.querySelectorAll('input[data-type="department"]').forEach(input => {
        const value = input.value.trim();
        if (value) departments.push(value);
    });

    // Collect automation options
    document.querySelectorAll('input[data-type="automation"]').forEach(input => {
        const value = input.value.trim();
        if (value) automation.push(value);
    });

    if (departments.length === 0 || automation.length === 0) {
        alert('Please ensure all dropdown types have at least one option.');
        return;
    }

    // Save to localStorage
    saveDropdownOptions({
        departments: departments,
        automationPotential: automation
    });

    // Update all dropdowns on the page
    updateAllDropdowns();

    // Close modal
    capstoneHub.closeModal();

    // Show success message
    showNotification('Dropdown options updated successfully!', 'success');
}

// Reset to default options
function resetDropdownOptions() {
    if (confirm('Are you sure you want to reset to default options? This will remove any custom options you\'ve added.')) {
        saveDropdownOptions(defaultDropdownOptions);
        capstoneHub.closeModal();
        showNotification('Dropdown options reset to defaults.', 'success');
    }
}

// Update all dropdowns with current options
function updateAllDropdowns() {
    const options = getDropdownOptions();

    // Update department filter
    const deptFilter = document.getElementById('department-filter');
    if (deptFilter) {
        const currentValue = deptFilter.value;
        deptFilter.innerHTML = '<option value="">All Departments</option>' +
            options.departments.map(dept => `<option value="${dept}">${dept}</option>`).join('');
        deptFilter.value = currentValue;
    }

    // Update automation filter
    const autoFilter = document.getElementById('automation-filter');
    if (autoFilter) {
        const currentValue = autoFilter.value;
        autoFilter.innerHTML = '<option value="">Automation Potential</option>' +
            options.automationPotential.map(auto => `<option value="${auto}">${auto}</option>`).join('');
        autoFilter.value = currentValue;
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    let bgColor;
    if (type === 'success') {
        bgColor = 'var(--success-color)';
    } else if (type === 'error') {
        bgColor = 'var(--error-color)';
    } else {
        bgColor = 'var(--primary-color)';
    }

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${bgColor};
        color: white;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Override the addProcess function to use dynamic options
const originalAddProcess = capstoneHub.addProcess;
capstoneHub.addProcess = function() {
    const options = getDropdownOptions();

    const form = `
        <form id="process-form">
            <div class="form-group mb-3">
                <label for="process-name">Process Name</label>
                <input type="text" id="process-name" class="form-control" required>
            </div>
            <div class="form-group mb-3">
                <label for="process-department">Department</label>
                <select id="process-department" class="form-control" required>
                    <option value="">Select Department</option>
                    ${options.departments.map(dept => `<option value="${dept}">${dept}</option>`).join('')}
                </select>
            </div>
            <div class="form-group mb-3">
                <label for="process-description">Description</label>
                <textarea id="process-description" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group mb-3">
                <label for="process-automation">Automation Potential</label>
                <select id="process-automation" class="form-control">
                    <option value="">Select Potential</option>
                    ${options.automationPotential.map(auto => `<option value="${auto}">${auto}</option>`).join('')}
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" onclick="capstoneHub.closeModal()">Cancel</button>
                <button type="submit" class="btn-primary">Add Process</button>
            </div>
        </form>
    `;
    this.showModal('Add Business Process', form);

    // Add form submit handler
    setTimeout(() => {
        const formElement = document.getElementById('process-form');
        if (formElement) {
            formElement.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.saveProcess();
            });
        }
    }, 100);
};

// Initialize dropdowns on page load
document.addEventListener('DOMContentLoaded', function() {
    updateAllDropdowns();
});

// Add animation styles
const animationStyles = `
<style>
@keyframes slideInRight {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOutRight {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(400px);
        opacity: 0;
    }
}
</style>
`;
document.head.insertAdjacentHTML('beforeend', animationStyles);

