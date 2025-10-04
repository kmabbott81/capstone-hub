#!/usr/bin/env python3
"""
Generate endpoint security coverage manifest
Scans all Flask routes and documents security controls
"""

import os
import sys
import json
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def extract_routes_from_file(filepath):
    """Extract route definitions from a Python file"""
    routes = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Look for @blueprint.route() decorator
        route_match = re.search(r"@\w+\.route\('([^']+)'(?:,\s*methods=\[([^\]]+)\])?", line)

        if route_match:
            path = route_match.group(1)
            methods_str = route_match.group(2)
            methods = []

            if methods_str:
                # Parse methods list
                methods = [m.strip().strip("'\"") for m in methods_str.split(',')]
            else:
                methods = ['GET']  # Default Flask method

            # Look ahead for decorators and function name
            decorators = []
            j = i - 1
            while j >= 0 and (lines[j].strip().startswith('@') or not lines[j].strip()):
                if lines[j].strip().startswith('@'):
                    decorators.append(lines[j].strip())
                j -= 1

            # Get function name
            func_match = re.search(r'def\s+(\w+)\(', lines[i + 1] if i + 1 < len(lines) else '')
            func_name = func_match.group(1) if func_match else 'unknown'

            # Determine security controls
            has_require_admin = any('@require_admin' in d for d in decorators)
            has_csrf_exempt = any('@csrf.exempt' in d for d in decorators)
            has_limiter = any('@limiter.limit' in d for d in decorators)

            # Extract rate limit if present
            rate_limit = None
            for d in decorators:
                limit_match = re.search(r'@limiter\.limit\(["\']([^"\']+)', d)
                if limit_match:
                    rate_limit = limit_match.group(1)

            # Create route entry for each method
            for method in methods:
                # CSRF applies to write operations
                requires_csrf = method in ['POST', 'PUT', 'PATCH', 'DELETE'] and not has_csrf_exempt

                routes.append({
                    'method': method,
                    'path': path,
                    'function': func_name,
                    'file': str(filepath.relative_to(project_root)),
                    'requires_admin': has_require_admin,
                    'csrf_protected': requires_csrf,
                    'rate_limit': rate_limit or 'n/a'
                })

        i += 1

    return routes

def main():
    """Generate complete route manifest"""
    routes_dir = project_root / 'src' / 'routes'
    all_routes = []

    # Scan all route files
    for py_file in routes_dir.glob('*.py'):
        if py_file.name == '__init__.py':
            continue

        file_routes = extract_routes_from_file(py_file)
        all_routes.extend(file_routes)

    # Sort by path, then method
    all_routes.sort(key=lambda r: (r['path'], r['method']))

    # Count security coverage
    write_routes = [r for r in all_routes if r['method'] in ['POST', 'PUT', 'PATCH', 'DELETE']]
    admin_protected = [r for r in write_routes if r['requires_admin']]
    csrf_protected = [r for r in write_routes if r['csrf_protected']]

    manifest = {
        'generated': '2025-10-04',
        'version': '0.36.0',
        'summary': {
            'total_routes': len(all_routes),
            'read_routes': len(all_routes) - len(write_routes),
            'write_routes': len(write_routes),
            'admin_protected': len(admin_protected),
            'csrf_protected': len(csrf_protected),
            'coverage': {
                'admin': f"{len(admin_protected)}/{len(write_routes)}",
                'csrf': f"{len(csrf_protected)}/{len(write_routes)}"
            }
        },
        'routes': all_routes
    }

    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
