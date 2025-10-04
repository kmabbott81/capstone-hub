# ChatGPT Audit Recommendations - Implementation Plan
**Date:** October 3, 2025
**Project:** HL Stearns AI Strategy Capstone Hub
**Goal:** Transform from basic CRUD app to command center for capstone project

---

## Executive Summary of ChatGPT's Analysis

**Bottom Line:** The app is "good enough" to store content and show progress, but needs 6 key upgrades to become your main project organizer:

1. ✅ Dates, reminders, and real timeline visualization
2. ✅ Edit everywhere + search/sort/pagination
3. ✅ Attachments/links (centralize all artifacts)
4. ✅ Advisor feedback capture (close the loop)
5. ✅ Export packets for each deliverable
6. ✅ Basic ops hardening (CSRF, rate limiting, backups)

---

## Official Capstone Timeline (From Program Guide)

### Required Deliverables & Due Dates

1. **Project Statement** - October 8, 2025 (5 days from now!)
2. **Conceptual Framework** - December 3, 2025
3. **Market/Competitive Analysis** - January 30, 2026
4. **Financial Analysis** - March 16, 2026
5. **Draft Report** - April 17, 2026
6. **Executive Summary** - May 13, 2026
7. **Presentation** - May 16-17, 2026
8. **Final Report** - May 29, 2026

### Critical Dates
- **Weekly advisor meetings** throughout
- **Feedback cycles** after each deliverable
- **Presentation rehearsals** in May

---

## 5-Day Sprint Plan (Oct 3-8)

### Day 1 (Friday Oct 4) - Edit Functions + Search/Sort
**Goal:** Complete basic CRUD for all sections

**Tasks:**
- [ ] Implement `editDeliverable(id)` + `updateDeliverable(id)`
- [ ] Implement `editAITechnology(id)` + `updateAITechnology(id)`
- [ ] Implement `editSoftwareTool(id)` + `updateSoftwareTool(id)`
- [ ] Implement `editResearchItem(id)` + `updateResearchItem(id)`
- [ ] Implement `editIntegration(id)` + `updateIntegration(id)`
- [ ] Add basic search bar to each section
- [ ] Add column sorting (click header to sort)

**Files to modify:**
- `src/static/app.js` (add edit functions following editProcess pattern)
- `src/static/index.html` (add search bars)

**Testing:**
- Edit each type of item
- Search for items by name
- Sort by different columns

---

### Day 2 (Saturday Oct 5) - Attachments System
**Goal:** Add ability to attach URLs/files to any item

**Tasks:**
- [ ] Create `attachments` table/model
- [ ] Add attachment fields: type, item_type, item_id, url, filename, description, created_at
- [ ] Create `/api/attachments` endpoints (GET, POST, DELETE)
- [ ] Add "Attachments" section to all item modals
- [ ] Add "📎 Attachments" badge/count to item cards
- [ ] Support URL links first (no file upload yet)

**New Files:**
- `src/models/attachment.py`
- `src/routes/attachments.py`

**Schema:**
```python
class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50))  # 'deliverable', 'process', etc.
    item_id = db.Column(db.Integer)
    attachment_type = db.Column(db.String(20))  # 'url', 'file'
    url = db.Column(db.String(500))
    filename = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Testing:**
- Add URL attachment to a deliverable
- View attachments list
- Delete attachment
- Verify attachments persist

---

### Day 3 (Sunday Oct 6) - Timeline Chart + Calendar Export
**Goal:** Visualize deliverables on actual timeline with due dates

**Tasks:**
- [ ] Seed 8 official deliverables with program dates
- [ ] Implement real timeline chart (CSS-based horizontal timeline)
- [ ] Add D-7 and D-1 badges to dashboard (days until next due date)
- [ ] Create `/api/calendar/ical` endpoint (iCalendar format)
- [ ] Add "📅 Subscribe to Calendar" button
- [ ] Show overdue items in red

**Timeline Chart Requirements:**
- Horizontal bar showing today's position
- Deliverables plotted by due date
- Color coding by status (not started/in progress/complete)
- Click to jump to deliverable details

**iCal Endpoint:**
```python
@app.route('/api/calendar/ical')
def export_ical():
    # Generate .ics file with all deliverable due dates
    # Format: BEGIN:VCALENDAR / BEGIN:VEVENT / DTSTART / DTEND / SUMMARY / END:VEVENT / END:VCALENDAR
```

**Testing:**
- View timeline chart on dashboard
- Verify 8 deliverables show correctly
- Download .ics file
- Import to Outlook/Google Calendar

---

### Day 4 (Monday Oct 7) - Advisor Feedback System
**Goal:** Track advisor comments and action items

**Tasks:**
- [ ] Create `feedback` table/model
- [ ] Add fields: deliverable_id, reviewer_name, date, comment, status (open/addressed)
- [ ] Create `/api/feedback` endpoints (GET, POST, PUT, DELETE)
- [ ] Add "Feedback" tab to deliverable detail view
- [ ] Add "💬 Feedback" badge with open count
- [ ] Add "Mark as Addressed" button for each comment

**New Files:**
- `src/models/feedback.py`
- `src/routes/feedback.py`

**Schema:**
```python
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deliverable_id = db.Column(db.Integer, db.ForeignKey('deliverable.id'))
    reviewer_name = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text)
    status = db.Column(db.String(20), default='open')  # 'open', 'addressed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Testing:**
- Add feedback to Project Statement deliverable
- Mark feedback as addressed
- View open feedback count
- Filter by status

---

### Day 5 (Tuesday Oct 8) - Export Packets + Security Hardening
**Goal:** Generate deliverable reports + secure the app

**Morning - Export Packets:**
- [ ] Create `/api/deliverables/<id>/export` endpoint
- [ ] Generate Markdown report with:
  - Deliverable title and description
  - Status and due date
  - Linked research items
  - Linked business processes
  - Attached files/URLs
  - Open feedback items
  - Open questions/notes
- [ ] Add "📄 Export Report" button to deliverable view
- [ ] Support Markdown download (PDF conversion later)

**Afternoon - Security Hardening:**
- [ ] Install Flask-WTF for CSRF protection
- [ ] Add CSRF tokens to all forms
- [ ] Install Flask-Limiter
- [ ] Add rate limiting to /api/auth/login (5 attempts per 15 min)
- [ ] Implement 30-minute idle session timeout
- [ ] Create nightly backup script (copy app.db to timestamped file)
- [ ] Add "💾 Backup Now" button to admin badge

**New Files:**
- `backup_database.py` (scheduled backup script)
- `requirements.txt` update (add Flask-WTF, Flask-Limiter)

**Testing:**
- Export deliverable packet (download markdown)
- Try login 6 times (should rate limit)
- Wait 31 minutes idle (should logout)
- Click backup button (verify timestamped .db file created)

---

## Week 2+ Enhancements (Optional)

### Pagination
- Add `?page=1&limit=25` query params to all list endpoints
- Add pagination controls to UI

### Email/Teams Notifications
- Create notification service (email via SendGrid or Teams webhook)
- Schedule weekly job: check deliverables due in 7 days, send reminder
- Daily job: check deliverables due tomorrow, send urgent reminder

### Database Relationships
**Currently flat schema - add foreign keys:**
```python
# In ResearchItem model
deliverable_id = db.Column(db.Integer, db.ForeignKey('deliverable.id'))

# In BusinessProcess model
deliverable_id = db.Column(db.Integer, db.ForeignKey('deliverable.id'))

# Many-to-many: Process ↔ Research
process_research = db.Table('process_research',
    db.Column('process_id', db.Integer, db.ForeignKey('business_process.id')),
    db.Column('research_id', db.Integer, db.ForeignKey('research_item.id'))
)
```

### Advanced Search
- Full-text search across all fields
- Filter by multiple criteria (date range, status, phase)
- Saved searches

### File Upload
- Upgrade attachments to support actual file uploads
- Store in Railway volume or S3
- Virus scanning
- File size limits

---

## Implementation Details

### 1. Edit Functions Pattern (Day 1)

All edit functions follow this pattern (example for deliverables):

```javascript
// In app.js CapstoneHub class

editDeliverable(id) {
    const item = this.data.deliverables.find(d => d.id === id);
    if (!item) {
        showNotification('Deliverable not found', 'error');
        return;
    }

    const form = `
        <form id="deliverable-form">
            <div class="form-group mb-3">
                <label for="deliverable-title">Title</label>
                <input type="text" id="deliverable-title" class="form-control"
                       value="${escapeHTML(item.title)}" required>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-description">Description</label>
                <textarea id="deliverable-description" class="form-control" rows="3">${escapeHTML(item.description || '')}</textarea>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-phase">Phase</label>
                <select id="deliverable-phase" class="form-control">
                    <option value="Planning" ${item.phase === 'Planning' ? 'selected' : ''}>Planning</option>
                    <option value="Research" ${item.phase === 'Research' ? 'selected' : ''}>Research</option>
                    <option value="Analysis" ${item.phase === 'Analysis' ? 'selected' : ''}>Analysis</option>
                    <option value="Writing" ${item.phase === 'Writing' ? 'selected' : ''}>Writing</option>
                    <option value="Review" ${item.phase === 'Review' ? 'selected' : ''}>Review</option>
                </select>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-due-date">Due Date</label>
                <input type="date" id="deliverable-due-date" class="form-control"
                       value="${item.due_date || ''}">
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-status">Status</label>
                <select id="deliverable-status" class="form-control">
                    <option value="Not Started" ${item.status === 'Not Started' ? 'selected' : ''}>Not Started</option>
                    <option value="In Progress" ${item.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="Complete" ${item.status === 'Complete' ? 'selected' : ''}>Complete</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" data-action="close-modal">Cancel</button>
                <button type="submit" class="btn-primary">Update Deliverable</button>
            </div>
        </form>
    `;

    this.showModal('Edit Deliverable', form);

    setTimeout(() => {
        const formElement = document.getElementById('deliverable-form');
        if (formElement) {
            formElement.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.updateDeliverable(id);
            });
        }
    }, 100);
}

async updateDeliverable(id) {
    const title = document.getElementById('deliverable-title').value;
    const description = document.getElementById('deliverable-description').value;
    const phase = document.getElementById('deliverable-phase').value;
    const dueDate = document.getElementById('deliverable-due-date').value;
    const status = document.getElementById('deliverable-status').value;

    try {
        const response = await fetch(`/api/deliverables/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                phase: phase,
                due_date: dueDate,
                status: status
            })
        });

        if (response.ok) {
            this.closeModal();
            this.loadDeliverables();
            this.updateDashboard();
            showNotification('Deliverable updated successfully!', 'success');
        } else {
            showNotification('Error updating deliverable', 'error');
        }
    } catch (error) {
        console.error('Error updating deliverable:', error);
        showNotification('Error updating deliverable', 'error');
    }
}
```

### 2. Search Implementation (Day 1)

Add search bar to each section:

```javascript
// In renderDeliverables() - add before the cards
const searchHTML = `
    <div class="search-bar">
        <input type="text" id="deliverables-search"
               placeholder="Search deliverables..."
               class="form-control">
    </div>
`;

// Add event listener
document.getElementById('deliverables-search')?.addEventListener('input', (e) => {
    this.filterDeliverables(e.target.value);
});

// Filter function
filterDeliverables(searchTerm) {
    const filtered = this.data.deliverables.filter(item => {
        const search = searchTerm.toLowerCase();
        return item.title?.toLowerCase().includes(search) ||
               item.description?.toLowerCase().includes(search) ||
               item.phase?.toLowerCase().includes(search);
    });

    // Re-render with filtered data
    this.renderDeliverablesFiltered(filtered);
}
```

### 3. Timeline Chart Implementation (Day 3)

CSS-based horizontal timeline:

```html
<div class="timeline-chart">
    <div class="timeline-header">
        <h3>Project Timeline</h3>
        <span class="days-remaining">Next: Project Statement in 5 days</span>
    </div>
    <div class="timeline-track">
        <div class="timeline-today-marker" style="left: 10%"></div>
        <!-- Deliverable markers -->
        <div class="timeline-item" style="left: 10%" data-id="1">
            <div class="timeline-dot status-in-progress"></div>
            <div class="timeline-label">Project Statement<br>Oct 8</div>
        </div>
        <div class="timeline-item" style="left: 30%" data-id="2">
            <div class="timeline-dot status-not-started"></div>
            <div class="timeline-label">Framework<br>Dec 3</div>
        </div>
        <!-- ... more deliverables ... -->
    </div>
</div>
```

### 4. CSRF Protection (Day 5)

```python
# In app.py
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Exempt API endpoints (use session validation instead)
@csrf.exempt
@app.route('/api/*')

# Or add CSRF token to all forms client-side
```

### 5. Rate Limiting (Day 5)

```python
# In app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# In auth.py
@auth_bp.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    # ... existing code
```

### 6. Session Timeout (Day 5)

```python
# In app.py
from flask import session
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
```

### 7. Backup Script (Day 5)

```python
# backup_database.py
import shutil
from datetime import datetime
import os

def backup_database():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source = 'src/database/app.db'
    destination = f'src/database/backups/app_backup_{timestamp}.db'

    os.makedirs('src/database/backups', exist_ok=True)
    shutil.copy2(source, destination)

    print(f'Backup created: {destination}')

    # Keep only last 30 backups
    cleanup_old_backups('src/database/backups', keep=30)

def cleanup_old_backups(backup_dir, keep=30):
    backups = sorted([
        os.path.join(backup_dir, f)
        for f in os.listdir(backup_dir)
        if f.startswith('app_backup_')
    ])

    if len(backups) > keep:
        for old_backup in backups[:-keep]:
            os.remove(old_backup)
            print(f'Removed old backup: {old_backup}')

if __name__ == '__main__':
    backup_database()
```

---

## Dependencies to Add

Update `requirements.txt`:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Cors==4.0.0
Flask-WTF==1.2.1          # CSRF protection
Flask-Limiter==3.5.0      # Rate limiting
python-dotenv==1.0.0
Werkzeug==2.3.7
icalendar==5.0.11         # iCal export
```

---

## Testing Checklist

### Day 1 - Edit + Search
- [ ] Edit deliverable, save, verify changes persist
- [ ] Edit AI technology, save, verify changes persist
- [ ] Edit software tool, save, verify changes persist
- [ ] Edit research item, save, verify changes persist
- [ ] Edit integration, save, verify changes persist
- [ ] Search deliverables by title
- [ ] Search processes by name
- [ ] Sort deliverables by due date
- [ ] Sort processes by department

### Day 2 - Attachments
- [ ] Add URL attachment to deliverable
- [ ] View attachments list
- [ ] Click attachment to open URL
- [ ] Delete attachment
- [ ] Reload page, verify attachment persists
- [ ] Add multiple attachments to one item

### Day 3 - Timeline + Calendar
- [ ] View timeline chart on dashboard
- [ ] Verify 8 deliverables plotted correctly
- [ ] Check "days remaining" badge accuracy
- [ ] Download .ics calendar file
- [ ] Import .ics to Outlook/Google Calendar
- [ ] Verify overdue items show in red

### Day 4 - Feedback
- [ ] Add feedback to Project Statement
- [ ] View feedback list
- [ ] Mark feedback as addressed
- [ ] Filter by open/addressed
- [ ] Delete feedback item
- [ ] Reload page, verify feedback persists

### Day 5 - Export + Security
- [ ] Export Project Statement packet (Markdown)
- [ ] Verify packet includes all sections
- [ ] Try login 6 times rapidly (should rate limit)
- [ ] Wait 31 minutes idle (should auto-logout)
- [ ] Click "Backup Now" button
- [ ] Verify timestamped .db file in backups folder
- [ ] Test all forms have CSRF protection

---

## Success Metrics

After 5-day sprint, the app should:

✅ **Replace scattered tools** - All project info in one place
✅ **Track progress visually** - Timeline shows where you are vs. deadlines
✅ **Capture feedback loops** - Advisor comments stored and tracked
✅ **Generate reports** - One-click export for each deliverable
✅ **Prevent data loss** - Automated backups + edit history
✅ **Secure operations** - CSRF, rate limiting, session timeout
✅ **Calendar integration** - Due dates sync to Outlook/Google

**Before:** Basic CRUD for documentation
**After:** Command center for managing entire capstone project

---

## Post-Sprint: Long-Term Roadmap

### Phase 2 (Oct 9-31) - Polish & Integrate
- Add email/Teams notifications for due dates
- Implement pagination for large lists
- Add database relationships (deliverable ↔ research)
- File upload support (not just URLs)
- PDF export (not just Markdown)

### Phase 3 (Nov) - Collaboration
- Multi-user support (advisor read-only access)
- Comments on all items (not just deliverables)
- Activity feed (who changed what when)
- Version history for key fields

### Phase 4 (Dec+) - Analytics
- Progress charts (deliverables by status)
- Time tracking (hours per phase)
- Risk dashboard (overdue items, blocked tasks)
- Final report generation (aggregate all data)

---

## Critical Path to Project Statement (Oct 8)

**You have 5 days until first deliverable!**

**Minimum viable for Oct 8:**
1. Create "Project Statement" deliverable with due date
2. Add research items linked to it
3. Attach any URLs (proposal docs, templates, etc.)
4. Export packet on Oct 8 to review completeness

**Don't wait for all features** - focus on Day 1-3 to support the immediate deadline.

---

## Questions Before Starting?

1. Should I implement Day 1 (Edit functions) now, or wait for approval?
2. Do you want to seed the 8 official deliverables now with the program dates?
3. Should attachments support both URLs and file uploads from day 1?
4. Do you want email notifications, Teams webhooks, or both?
5. Should the timeline chart be the main dashboard view, or a separate section?

Let me know what you want to tackle first, and I'll start coding!
