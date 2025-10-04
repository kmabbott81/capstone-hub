#!/usr/bin/env python3
"""Apply escapeHTML to all user data in remaining render functions"""
import re

with open('src/static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find renderProcesses and add escapeHTML
processes_old = """        container.innerHTML = this.data.processes.map(process => {
            const name = process.name || 'Untitled Process';
            const dept = process.department || 'Not specified';
            const automation = process.automation_potential || 'Not Set';
            const desc = process.description || 'No description provided';
            const currentState = process.current_state || 'Not documented';
            const painPoints = process.pain_points || '';
            const aiRec = process.ai_recommendations || '';
            const priority = process.priority_score || '';"""

processes_new = """        container.innerHTML = this.data.processes.map(process => {
            const name = escapeHTML(process.name || 'Untitled Process');
            const dept = escapeHTML(process.department || 'Not specified');
            const automation = escapeHTML(process.automation_potential || 'Not Set');
            const desc = escapeHTML(process.description || 'No description provided');
            const currentState = escapeHTML(process.current_state || 'Not documented');
            const painPoints = escapeHTML(process.pain_points || '');
            const aiRec = escapeHTML(process.ai_recommendations || '');
            const priority = escapeHTML(process.priority_score || '');"""

content = content.replace(processes_old, processes_new)

# Find renderAITechnologies and add escapeHTML
ai_old = """        container.innerHTML = this.data.aiTechnologies.map(tech => {
            const name = tech.name || 'Untitled';
            const category = tech.category || 'Uncategorized';
            const desc = tech.description || 'No description';
            const useCase = tech.use_case || '';
            const maturity = tech.maturity_level || 'Unknown';"""

ai_new = """        container.innerHTML = this.data.aiTechnologies.map(tech => {
            const name = escapeHTML(tech.name || 'Untitled');
            const category = escapeHTML(tech.category || 'Uncategorized');
            const desc = escapeHTML(tech.description || 'No description');
            const useCase = escapeHTML(tech.use_case || '');
            const maturity = escapeHTML(tech.maturity_level || 'Unknown');"""

content = content.replace(ai_old, ai_new)

# Find renderResearchItems and add escapeHTML
research_old = """        container.innerHTML = this.data.researchItems.map(item => {
            const title = item.title || 'Untitled';
            const type = item.research_type || 'General';
            const method = item.research_method || 'Not specified';
            const desc = item.description || 'No description';
            const source = item.source || '';
            const findings = item.key_findings || '';"""

research_new = """        container.innerHTML = this.data.researchItems.map(item => {
            const title = escapeHTML(item.title || 'Untitled');
            const type = escapeHTML(item.research_type || 'General');
            const method = escapeHTML(item.research_method || 'Not specified');
            const desc = escapeHTML(item.description || 'No description');
            const source = escapeHTML(item.source || '');
            const findings = escapeHTML(item.key_findings || '');"""

content = content.replace(research_old, research_new)

# Find renderIntegrations and add escapeHTML
integrations_old = """        container.innerHTML = this.data.integrations.map(item => {
            const name = item.name || 'Untitled Integration';
            const type = item.integration_type || 'Unknown';
            const status = item.status || 'Inactive';
            const desc = item.description || 'No description';
            const endpoint = item.api_endpoint || '';"""

integrations_new = """        container.innerHTML = this.data.integrations.map(item => {
            const name = escapeHTML(item.name || 'Untitled Integration');
            const type = escapeHTML(item.integration_type || 'Unknown');
            const status = escapeHTML(item.status || 'Inactive');
            const desc = escapeHTML(item.description || 'No description');
            const endpoint = escapeHTML(item.api_endpoint || '');"""

content = content.replace(integrations_old, integrations_new)

with open('src/static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied escapeHTML to all render functions")
