"""
Logging configuration with sensitive field redaction
"""

import logging
import logging.handlers
import os
import re
from pathlib import Path


class SensitiveDataFilter(logging.Filter):
    """Filter to redact sensitive information from logs"""

    SENSITIVE_PATTERNS = [
        (re.compile(r'("password"\s*:\s*)"[^"]*"', re.IGNORECASE), r'\1"[REDACTED]"'),
        (re.compile(r'("token"\s*:\s*)"[^"]*"', re.IGNORECASE), r'\1"[REDACTED]"'),
        (re.compile(r'("key"\s*:\s*)"[^"]*"', re.IGNORECASE), r'\1"[REDACTED]"'),
        (re.compile(r'("secret"\s*:\s*)"[^"]*"', re.IGNORECASE), r'\1"[REDACTED]"'),
        (re.compile(r'(password=)[^\s&]+', re.IGNORECASE), r'\1[REDACTED]'),
        (re.compile(r'(api[_-]?key=)[^\s&]+', re.IGNORECASE), r'\1[REDACTED]'),
        (re.compile(r'(Bearer\s+)[^\s]+', re.IGNORECASE), r'\1[REDACTED]'),
    ]

    def filter(self, record):
        """Redact sensitive information from log message"""
        if isinstance(record.msg, str):
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                record.msg = pattern.sub(replacement, record.msg)

        # Also redact from args if present
        if record.args:
            redacted_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    for pattern, replacement in self.SENSITIVE_PATTERNS:
                        arg = pattern.sub(replacement, arg)
                redacted_args.append(arg)
            record.args = tuple(redacted_args)

        return True


def setup_logging(app):
    """Configure rotating file logs with INFO level for production"""

    # Determine log level from environment
    log_level_name = os.environ.get('LOG_LEVEL', 'INFO' if app.config.get('ENV') == 'production' else 'DEBUG')
    log_level = getattr(logging, log_level_name, logging.INFO)

    # Create logs directory
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)

    # Application log (general info)
    app_log_file = log_dir / 'app.log'
    app_handler = logging.handlers.RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    app_handler.setLevel(log_level)
    app_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    app_handler.addFilter(SensitiveDataFilter())

    # Error log (errors and above)
    error_log_file = log_dir / 'error.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    error_handler.addFilter(SensitiveDataFilter())

    # Console handler (for Railway logs)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(name)s: %(message)s'
    ))
    console_handler.addFilter(SensitiveDataFilter())

    # Configure Flask app logger
    app.logger.setLevel(log_level)
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(console_handler)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove default handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)

    # Log startup message
    app.logger.info(f"Logging configured: level={log_level_name}, handlers={len(app.logger.handlers)}")
    app.logger.info(f"Log files: {app_log_file}, {error_log_file}")

    return app.logger
