# Capstone Hub

![Version](https://img.shields.io/badge/version-v0.36.1--p1b--maint-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.0%2B-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Security](https://img.shields.io/badge/security-Phase%201b%20Complete-brightgreen)

A secure, production-grade Flask application for managing capstone project deliverables, business processes, AI technologies, and research items.

---

## Features

### Security (Phase 1 & 1b Complete)
- ✅ **Role-Based Access Control (RBAC)** - Admin and Viewer roles with distinct permissions
- ✅ **Password Hashing** - PBKDF2-SHA256 via werkzeug.security
- ✅ **Session Management** - 30-minute idle timeout with secure cookies
- ✅ **CSRF Protection** - Flask-WTF CSRF tokens for all state-changing operations
- ✅ **Rate Limiting** - 5 login attempts per 15 minutes per IP
- ✅ **Security Headers** - CSP, X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- ✅ **Log Redaction** - Automatic filtering of passwords, tokens, keys from logs
- ✅ **Continuous Verification** - Automated smoke tests on every push

### Core Functionality
- **Deliverables Management** - Track project deliverables with status, dates, and descriptions
- **Business Processes** - Document and manage business process workflows
- **AI Technologies** - Catalog AI tools and technologies used in projects
- **Software Tools** - Track software development tools and integrations
- **Research Items** - Organize research findings and references
- **Advanced Analytics** - Generate reports and visualizations (coming soon)

### Operations
- **Automated Testing** - Pytest test suite with CI/CD integration
- **Build Verification** - Pre-deployment smoke tests and security audits
- **Environment Validation** - Automated environment variable checking
- **Rotating Logs** - 10MB × 5 backups with automatic rotation
- **Backup System** - Automated database backups with 14-day retention

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/capstone-hub.git
cd capstone-hub

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.sample .env

# Generate secure SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
# Add to .env: SECRET_KEY=<generated-key>

# Generate admin password hash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))"
# Add to .env: ADMIN_PASSWORD_HASH=<generated-hash>

# Run application
python src/main.py
```

Application will be available at http://localhost:5000

### Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# Set environment variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set ADMIN_PASSWORD_HASH="pbkdf2:sha256:..."
railway variables set FLASK_ENV="production"
railway variables set LOG_LEVEL="INFO"

# Deploy
railway up

# Monitor
railway logs
```

---

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | Flask session encryption key (64+ chars) | `abc123...` |
| `ADMIN_PASSWORD_HASH` | Yes* | Hashed admin password (production) | `pbkdf2:sha256:...` |
| `ADMIN_PASSWORD` | Yes* | Plain admin password (development only) | `MyPassword123` |
| `VIEWER_PASSWORD_HASH` | No | Hashed viewer password (production) | `pbkdf2:sha256:...` |
| `VIEWER_PASSWORD` | No | Plain viewer password (development) | `ViewerPass` |
| `FLASK_ENV` | No | Environment (production/development) | `production` |
| `LOG_LEVEL` | No | Logging verbosity | `INFO` |
| `DATABASE_URL` | No | Database connection string | `sqlite:///...` |
| `ENABLE_DEBUG_ROUTES` | No | Enable debug routes (0 or unset) | `0` |

*One of `ADMIN_PASSWORD_HASH` or `ADMIN_PASSWORD` is required.

See [.env.sample](.env.sample) for complete documentation.

---

## Testing

### Run All Tests
```bash
# Complete smoke test suite
make smoke

# Or individual components
make verify-build    # Tests + security audit + manifest
make validate-env    # Environment validation
make test           # Pytest suite only
make audit          # Security audit only
```

### Verification Scripts
```bash
# Build verification
bash scripts/verify_build.sh

# Environment validation
python scripts/validate_env.py

# Admin guard verification
python scripts/verify_admin_guard.py

# Rate limit verification
bash scripts/prove_rate_limit.sh

# Security headers verification
python scripts/verify_headers.py
```

---

## Architecture

```
capstone-hub/
├── src/
│   ├── main.py              # Application entry point
│   ├── extensions.py        # Flask extensions (CSRF, rate limiter)
│   ├── logging_config.py    # Log configuration with redaction
│   ├── models/              # SQLAlchemy database models
│   ├── routes/              # API endpoints and blueprints
│   └── static/              # Frontend assets
├── scripts/
│   ├── verify_build.sh      # Build verification suite
│   ├── validate_env.py      # Environment validator
│   ├── verify_admin_guard.py # Admin protection verification
│   ├── prove_rate_limit.sh  # Rate limit proof
│   └── verify_headers.py    # Security headers verification
├── tests/                   # Pytest test suite
├── security/
│   ├── build_snapshot/      # Verification artifacts
│   └── endpoint_coverage/   # Route manifests
├── docs/
│   ├── DEPLOYMENT.md        # Detailed deployment guide
│   ├── OPS_CHECKLIST.md     # Operations runbook
│   └── CHANGE_CONTROL.md    # Change management procedures
├── .github/
│   └── workflows/
│       └── preflight.yml    # CI/CD pipeline
├── CHANGELOG.md             # Version history
├── SECURITY.md              # Security policy
└── Makefile                 # Automation commands
```

---

## Security

### Authentication
- **Admin Role**: Full access to all features (create, read, update, delete)
- **Viewer Role**: Read-only access (view and export only)

### Default Credentials (Development Only)
- **Admin**: Set via `ADMIN_PASSWORD` environment variable
- **Viewer**: "CapstoneView" (configurable via `VIEWER_PASSWORD`)

**⚠️ IMPORTANT**: Always use hashed passwords in production environments.

### Security Best Practices
1. Generate strong `SECRET_KEY` (64+ characters)
2. Use password hashing in production (`ADMIN_PASSWORD_HASH`)
3. Enable HTTPS (automatic on Railway)
4. Set `FLASK_ENV=production`
5. Keep `ENABLE_DEBUG_ROUTES=0` or unset
6. Review logs regularly for security issues
7. Run `python -m pip_audit` before deployment

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

---

## Operations

### Pre-Deployment Checklist
- [ ] Run `make smoke` - all tests pass
- [ ] Run `python -m pip_audit` - no vulnerabilities
- [ ] Verify environment variables set
- [ ] Review CHANGELOG.md
- [ ] Create version tag
- [ ] Update documentation

### Post-Deployment Verification
- [ ] Application responds: `curl https://your-app.up.railway.app/`
- [ ] Security headers present: `python scripts/verify_headers.py`
- [ ] Authentication works: Test login flow
- [ ] Logs clean: `railway logs | grep ERROR`

### Monitoring
```bash
# View logs
railway logs
make logs

# Check status
railway status

# View metrics
# Access Railway dashboard
```

### Backup and Restore
```bash
# Backup database
cp src/database/app.db backups/app.db.$(date +%Y%m%d)

# Railway backup
railway run cp /app/src/database/app.db /backups/
```

See [docs/OPS_CHECKLIST.md](docs/OPS_CHECKLIST.md) for complete operations guide.

---

## CI/CD Pipeline

Automated continuous verification via GitHub Actions:

- **Trigger**: Every push or PR to `main` branch
- **Matrix**: Tests on Windows and Ubuntu
- **Steps**:
  1. Install dependencies
  2. Run pytest suite
  3. Run security audit (pip-audit)
  4. Generate route manifest
  5. Run smoke tests

See [.github/workflows/preflight.yml](.github/workflows/preflight.yml)

---

## Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment guide (local + Railway)
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability disclosure
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[docs/OPS_CHECKLIST.md](docs/OPS_CHECKLIST.md)** - Operations runbook
- **[docs/CHANGE_CONTROL.md](docs/CHANGE_CONTROL.md)** - Change management procedures
- **[.env.sample](.env.sample)** - Environment variable documentation

---

## Troubleshooting

### Application Won't Start
```bash
# Check environment variables
python scripts/validate_env.py

# View logs
railway logs | grep ERROR

# Restart service
railway restart
```

### Authentication Failing
```bash
# Verify password hash
railway variables | grep ADMIN_PASSWORD

# Test hash generation
python -c "from werkzeug.security import generate_password_hash, check_password_hash; h=generate_password_hash('test'); print(h); print(check_password_hash(h, 'test'))"
```

### High Error Rate
```bash
# Check recent logs
railway logs --since 1h | grep ERROR

# Review error log file
railway run cat logs/error.log

# Rollback if needed
railway rollback
```

See [docs/OPS_CHECKLIST.md](docs/OPS_CHECKLIST.md) for complete troubleshooting guide.

---

## Version History

- **v0.36.1-p1b-maint** (2025-10-04) - Maintenance patch: CI/CD, docs, header verification
- **v0.36.1-sealed** (2025-10-04) - Phase 1b sealed with proofs and ops artifacts
- **v0.36.1-phase1b** (2025-10-04) - Phase 1b pre-production hardening
- **v0.36.0-audit-remediated** (2025-10-03) - External audit gap remediation
- **v0.36.0** (2025-10-03) - Phase 1 Security implementation

See [CHANGELOG.md](CHANGELOG.md) for complete history.

---

## Contributing

### Development Workflow
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Description"`
3. Run tests: `make smoke`
4. Push and create PR: `git push origin feature/your-feature`

### Code Review
- All changes require peer review
- Security-sensitive changes require security lead approval
- CI/CD must pass before merge

See [docs/CHANGE_CONTROL.md](docs/CHANGE_CONTROL.md) for detailed procedures.

---

## License

MIT License - see LICENSE file for details

---

## Support

- **Documentation**: See docs/ directory
- **Issues**: Create GitHub issue with details
- **Security**: security@hlstearns.local
- **Privacy**: privacy@hlstearns.local

---

## Governance and Compliance

- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability disclosure
- **[PRIVACY.md](PRIVACY.md)** - Privacy policy and data subject rights
- **[DATA_RETENTION.md](DATA_RETENTION.md)** - Data retention and purge policies

These policies ensure Capstone Hub meets academic and professional standards for data governance, privacy protection, and security compliance.

---

## Acknowledgments

Built for MBA Capstone Program at University of Oregon.

**Security Audits:**
- Phase 1 Security Audit (2025-10-03)
- Phase 1b Pre-Production Hardening (2025-10-04)

🤖 Developed with assistance from [Claude Code](https://claude.com/claude-code)

---

**Last Updated**: 2025-10-04
**Current Version**: v0.36.1-p1b-maint
**Status**: Production-Ready for Academic Deployment
