#!/usr/bin/env python3
"""
Telemetry Lite - Privacy-Safe Operational Observability
Records only uptime and error counts (no PII, no tracking)
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import re

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def get_database_path():
    """Get path to application database"""
    return Path(__file__).parent.parent / 'src' / 'database' / 'app.db'


def get_log_dir():
    """Get path to logs directory"""
    return Path(__file__).parent.parent / 'logs'


def get_telemetry_output():
    """Get path to telemetry summary log"""
    log_dir = get_log_dir()
    log_dir.mkdir(exist_ok=True)
    return log_dir / 'telemetry_summary.log'


def check_database_health():
    """Check if database is accessible and healthy"""
    db_path = get_database_path()

    if not db_path.exists():
        return {
            'healthy': False,
            'error': 'Database file not found'
        }

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        # Count records in main tables
        counts = {}
        for table in ['deliverables', 'business_process', 'ai_technology',
                      'software_tool', 'research_item', 'integration']:
            if table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]

        conn.close()

        return {
            'healthy': True,
            'tables': len(tables),
            'record_counts': counts
        }

    except Exception as e:
        return {
            'healthy': False,
            'error': str(e)
        }


def analyze_logs(days=7):
    """Analyze log files for errors and patterns (privacy-safe)"""
    log_dir = get_log_dir()
    error_log = log_dir / 'error.log'
    app_log = log_dir / 'app.log'

    stats = {
        'error_count': 0,
        'warning_count': 0,
        'critical_count': 0,
        'auth_failures': 0,
        'rate_limit_hits': 0,
        'csp_violations': 0,
        'error_types': {}
    }

    # Parse error log
    if error_log.exists():
        try:
            with open(error_log, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if '[ERROR]' in line:
                        stats['error_count'] += 1
                        # Extract error type (no PII)
                        match = re.search(r'([A-Z][a-zA-Z]+Error)', line)
                        if match:
                            error_type = match.group(1)
                            stats['error_types'][error_type] = stats['error_types'].get(error_type, 0) + 1

                    elif '[WARNING]' in line:
                        stats['warning_count'] += 1

                    elif '[CRITICAL]' in line:
                        stats['critical_count'] += 1

        except Exception as e:
            stats['log_parse_error'] = str(e)

    # Parse app log for security events
    if app_log.exists():
        try:
            with open(app_log, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if 'Authentication required' in line or 'Invalid password' in line:
                        stats['auth_failures'] += 1

                    elif '429' in line or 'rate limit' in line.lower():
                        stats['rate_limit_hits'] += 1

        except Exception as e:
            stats['app_log_parse_error'] = str(e)

    # Count CSP violations
    csp_log = log_dir / 'csp_reports.log'
    if csp_log.exists():
        try:
            with open(csp_log, 'r', encoding='utf-8', errors='ignore') as f:
                stats['csp_violations'] = sum(1 for line in f if 'CSPVIOLATION' in line)
        except:
            pass

    return stats


def calculate_uptime_estimate():
    """Estimate uptime based on log timestamps (not real-time monitoring)"""
    log_dir = get_log_dir()
    app_log = log_dir / 'app.log'

    if not app_log.exists():
        return {'available': False, 'reason': 'No log file'}

    try:
        # Find first and last log entries
        with open(app_log, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        if len(lines) < 2:
            return {'available': False, 'reason': 'Insufficient log data'}

        # Parse first and last timestamps
        first_line = lines[0]
        last_line = lines[-1]

        # Extract timestamp (format: YYYY-MM-DD HH:MM:SS)
        timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'

        first_match = re.search(timestamp_pattern, first_line)
        last_match = re.search(timestamp_pattern, last_line)

        if not first_match or not last_match:
            return {'available': False, 'reason': 'Could not parse timestamps'}

        first_time = datetime.strptime(first_match.group(1), '%Y-%m-%d %H:%M:%S')
        last_time = datetime.strptime(last_match.group(1), '%Y-%m-%d %H:%M:%S')

        duration = last_time - first_time

        return {
            'available': True,
            'first_log': first_time.isoformat(),
            'last_log': last_time.isoformat(),
            'duration_hours': duration.total_seconds() / 3600,
            'log_lines': len(lines)
        }

    except Exception as e:
        return {'available': False, 'reason': str(e)}


def generate_health_summary():
    """Generate weekly health summary (privacy-safe)"""
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Capstone Hub - Telemetry Lite Summary{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"Generated: {datetime.now().isoformat()}")
    print(f"Period: Last 7 days\n")

    summary = {
        'timestamp': datetime.now().isoformat(),
        'period_days': 7
    }

    # Database health
    print(f"{Colors.BOLD}Database Health:{Colors.END}")
    db_health = check_database_health()
    summary['database'] = db_health

    if db_health['healthy']:
        print(f"  {Colors.GREEN}[OK]{Colors.END} Database accessible")
        print(f"  Tables: {db_health['tables']}")
        if db_health.get('record_counts'):
            print(f"  Record Counts:")
            for table, count in db_health['record_counts'].items():
                print(f"    - {table}: {count}")
    else:
        print(f"  {Colors.RED}[X]{Colors.END} Database issue: {db_health.get('error', 'Unknown')}")

    # Log analysis
    print(f"\n{Colors.BOLD}Error Statistics (Last 7 Days):{Colors.END}")
    log_stats = analyze_logs(days=7)
    summary['logs'] = log_stats

    if log_stats['error_count'] == 0:
        print(f"  {Colors.GREEN}[OK]{Colors.END} No errors logged")
    else:
        print(f"  {Colors.YELLOW}[!]{Colors.END} Errors: {log_stats['error_count']}")
        if log_stats['error_types']:
            print(f"  Error Types:")
            for error_type, count in sorted(log_stats['error_types'].items(), key=lambda x: x[1], reverse=True):
                print(f"    - {error_type}: {count}")

    if log_stats['warning_count'] > 0:
        print(f"  {Colors.YELLOW}[!]{Colors.END} Warnings: {log_stats['warning_count']}")

    if log_stats['critical_count'] > 0:
        print(f"  {Colors.RED}[X]{Colors.END} Critical: {log_stats['critical_count']}")

    # Security events
    print(f"\n{Colors.BOLD}Security Events:{Colors.END}")
    if log_stats['auth_failures'] == 0:
        print(f"  {Colors.GREEN}[OK]{Colors.END} No authentication failures")
    else:
        print(f"  {Colors.YELLOW}[!]{Colors.END} Auth failures: {log_stats['auth_failures']}")

    if log_stats['rate_limit_hits'] == 0:
        print(f"  {Colors.GREEN}[OK]{Colors.END} No rate limit violations")
    else:
        print(f"  {Colors.YELLOW}[!]{Colors.END} Rate limits hit: {log_stats['rate_limit_hits']}")

    if log_stats['csp_violations'] == 0:
        print(f"  {Colors.GREEN}[OK]{Colors.END} No CSP violations")
    else:
        print(f"  {Colors.YELLOW}[!]{Colors.END} CSP violations: {log_stats['csp_violations']}")

    # Uptime estimate
    print(f"\n{Colors.BOLD}Uptime Estimate:{Colors.END}")
    uptime = calculate_uptime_estimate()
    summary['uptime'] = uptime

    if uptime['available']:
        print(f"  {Colors.GREEN}[OK]{Colors.END} Log span: {uptime['duration_hours']:.1f} hours")
        print(f"  First log: {uptime['first_log']}")
        print(f"  Last log: {uptime['last_log']}")
        print(f"  Log lines: {uptime['log_lines']}")
    else:
        print(f"  {Colors.YELLOW}[!]{Colors.END} Uptime data not available: {uptime.get('reason', 'Unknown')}")

    # Overall health score
    print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")

    health_score = 100
    issues = []

    if not db_health['healthy']:
        health_score -= 40
        issues.append("Database inaccessible")

    if log_stats['critical_count'] > 0:
        health_score -= 30
        issues.append(f"{log_stats['critical_count']} critical errors")

    if log_stats['error_count'] > 10:
        health_score -= 20
        issues.append(f"{log_stats['error_count']} errors")

    if log_stats['auth_failures'] > 20:
        health_score -= 10
        issues.append(f"{log_stats['auth_failures']} auth failures")

    summary['health_score'] = max(0, health_score)
    summary['issues'] = issues

    if health_score >= 90:
        print(f"{Colors.BOLD}{Colors.GREEN}[EXCELLENT] Health Score: {health_score}/100{Colors.END}")
    elif health_score >= 70:
        print(f"{Colors.BOLD}{Colors.YELLOW}[GOOD] Health Score: {health_score}/100{Colors.END}")
    else:
        print(f"{Colors.BOLD}{Colors.RED}[ATTENTION NEEDED] Health Score: {health_score}/100{Colors.END}")

    if issues:
        print(f"\n{Colors.BOLD}Issues Detected:{Colors.END}")
        for issue in issues:
            print(f"  - {issue}")

    print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")

    # Save to log file
    output_file = get_telemetry_output()
    try:
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*70}\n")
            f.write(f"Telemetry Summary - {datetime.now().isoformat()}\n")
            f.write(f"{'='*70}\n")
            f.write(json.dumps(summary, indent=2))
            f.write(f"\n{'='*70}\n\n")

        print(f"Summary saved to: {output_file}")

    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.END} Failed to save summary: {e}")

    return health_score


def main():
    """Main telemetry collection entry point"""
    try:
        health_score = generate_health_summary()

        # Exit code based on health score
        if health_score >= 70:
            return 0
        elif health_score >= 50:
            return 1
        else:
            return 2

    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.END} Telemetry error: {e}")
        return 2


if __name__ == '__main__':
    sys.exit(main())
