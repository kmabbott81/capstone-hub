#!/usr/bin/env python3
"""Add escapeHTML() to all user data in render functions"""
import re

with open('src/static/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all render functions and escape user data fields
# Pattern: const varName = item.field || 'default';
# Replace with: const varName = escapeHTML(item.field || 'default');

# List of common user-input fields that need escaping
user_fields = [
    'name', 'title', 'description', 'department', 'category',
    'type', 'method', 'source', 'findings', 'use_case', 'maturity',
    'desc', 'endpoint', 'automation', 'currentState', 'painPoints',
    'aiRec', 'priority', 'useCase', 'maturity_level', 'platform_provider',
    'research_type', 'research_method', 'key_findings', 'integration_type',
    'api_endpoint'
]

# Apply escapeHTML to variable assignments within render functions
for field in user_fields:
    # Pattern 1: const field = item.field || 'default';
    pattern1 = rf"(const {field} = )(?!escapeHTML\()([\w.]+\[['\"][\w_]+['\"]\]|\w+\.[\w_]+)( \|\| [^;]+);"
    replacement1 = rf"\1escapeHTML(\2\3);"
    content = re.sub(pattern1, replacement1, content)

    # Pattern 2: const field = item.field || '';
    pattern2 = rf"(const {field} = )(?!escapeHTML\()(\w+\.{field})( \|\| [^;]+);"
    replacement2 = rf"\1escapeHTML(\2\3);"
    content = re.sub(pattern2, replacement2, content)

with open('src/static/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("XSS escaping added to all render functions")
