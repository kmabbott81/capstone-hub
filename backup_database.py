#!/usr/bin/env python3
"""
Database Backup Script for Capstone Hub
Creates timestamped backups of the SQLite database
"""

import shutil
import os
from datetime import datetime


def backup_database():
    """Create timestamped backup of database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source = 'src/database/app.db'
    backup_dir = 'src/database/backups'
    destination = f'{backup_dir}/app_{timestamp}.db'

    # Create backups directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Verify source exists
    if not os.path.exists(source):
        print(f'❌ Error: Source database not found: {source}')
        return None

    # Copy database
    try:
        shutil.copy2(source, destination)
        file_size = os.path.getsize(destination) / 1024  # KB
        print(f'✅ Backup created: {destination} ({file_size:.1f} KB)')

        # Cleanup old backups (keep last 14)
        cleanup_old_backups(backup_dir, keep=14)

        return destination

    except Exception as e:
        print(f'❌ Backup failed: {str(e)}')
        return None


def cleanup_old_backups(backup_dir, keep=14):
    """Remove old backups, keeping only the most recent ones"""
    try:
        backups = sorted([
            os.path.join(backup_dir, f)
            for f in os.listdir(backup_dir)
            if f.startswith('app_') and f.endswith('.db')
        ])

        if len(backups) > keep:
            removed_count = 0
            for old_backup in backups[:-keep]:
                os.remove(old_backup)
                removed_count += 1
                print(f'🗑️  Removed old backup: {os.path.basename(old_backup)}')

            if removed_count > 0:
                print(f'Kept {keep} most recent backups, removed {removed_count} old backup(s)')

    except Exception as e:
        print(f'⚠️  Warning: Cleanup failed: {str(e)}')


def list_backups():
    """List all existing backups"""
    backup_dir = 'src/database/backups'

    if not os.path.exists(backup_dir):
        print('No backups directory found')
        return []

    backups = sorted([
        f for f in os.listdir(backup_dir)
        if f.startswith('app_') and f.endswith('.db')
    ], reverse=True)

    if not backups:
        print('No backups found')
        return []

    print(f'\n📦 Found {len(backups)} backup(s):')
    for backup in backups:
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path) / 1024
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f'  • {backup} ({size:.1f} KB) - {mtime.strftime("%Y-%m-%d %H:%M:%S")}')

    return backups


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_backups()
    else:
        print('🔄 Starting database backup...')
        result = backup_database()
        if result:
            print('\n✅ Backup completed successfully')
            sys.exit(0)
        else:
            print('\n❌ Backup failed')
            sys.exit(1)
