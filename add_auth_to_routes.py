#!/usr/bin/env python3
"""Add @require_admin decorator to all write routes"""
import os
import re

routes_dir = 'src/routes'
route_files = [
    'deliverables.py',
    'ai_technologies.py',
    'research_items.py',
    'integrations.py',
    'software_tools.py'
]

for filename in route_files:
    filepath = os.path.join(routes_dir, filename)

    if not os.path.exists(filepath):
        print(f"⚠️  {filename} not found, skipping")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if auth import already exists
    if 'from src.routes.auth import require_admin' in content:
        print(f"✅ {filename} already has auth import")
        continue

    # Add import after other imports
    import_pattern = r'(from src\.models\.database import db\n)'
    replacement = r'\1from src.routes.auth import require_admin\n'
    content = re.sub(import_pattern, replacement, content)

    # Add @require_admin to POST routes
    content = re.sub(
        r"(@[\w_]+\.route\(['\"][^'\"]+['\"], methods=\['POST'\]\)\n)(def )",
        r'\1@require_admin\n\2',
        content
    )

    # Add @require_admin to PUT routes
    content = re.sub(
        r"(@[\w_]+\.route\(['\"][^'\"]+['\"], methods=\['PUT'\]\)\n)(def )",
        r'\1@require_admin\n\2',
        content
    )

    # Add @require_admin to DELETE routes
    content = re.sub(
        r"(@[\w_]+\.route\(['\"][^'\"]+['\"], methods=\['DELETE'\]\)\n)(def )",
        r'\1@require_admin\n\2',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {filename}")

print("\n✅ All route files updated with @require_admin decorator")
