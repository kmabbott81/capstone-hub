# Quick Start Guide for AI Agents

## Project Context
You are working on Kyle Mabbott's Enhanced Capstone Hub for his HL Stearns AI Strategy capstone project. This is a Flask web application that manages research, experiments, and business process analysis for an MBA capstone project.

## Current Live Application
- **URL**: https://77h9ikc6780p.manus.space
- **Admin Password**: `HLStearns2025!`
- **Status**: Functional but missing content creation features

## Immediate Task Priority
The user can log in as admin but cannot add any content. Your first task is to implement the "Add New" buttons and forms for content creation.

## Quick Setup
```bash
cd capstone-hub-complete-dev-package
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

## Key Files to Understand
1. **src/static/index.html** - Main application interface
2. **src/static/app.js** - Frontend JavaScript logic
3. **src/static/auth-fixed.js** - Authentication system
4. **src/main.py** - Flask application entry point
5. **src/routes/** - API endpoints (already implemented)
6. **src/models/** - Database models (already implemented)

## What's Working
- Authentication system (admin/viewer roles)
- Navigation between sections
- Responsive design
- Backend API endpoints
- Database models

## What's Missing (Your Tasks)
1. **Add buttons** - "Add New" buttons visible only to admin users
2. **Modal forms** - Pop-up forms for creating content
3. **API integration** - Connect forms to backend endpoints
4. **Edit/Delete buttons** - For existing content management
5. **File upload** - For images and documents

## Architecture Overview
- **Frontend**: Vanilla JavaScript, no frameworks
- **Backend**: Flask with SQLAlchemy
- **Database**: SQLite (app.db)
- **Authentication**: Client-side localStorage
- **Styling**: Custom CSS with responsive design

## User Workflow
1. User visits site (viewer mode by default)
2. User clicks 🔐 button and enters admin password
3. User sees small "👑 Admin" badge in bottom right
4. User should see "Add New" buttons in each section (MISSING)
5. User clicks "Add New" and fills out form (MISSING)
6. Content is saved and displayed (MISSING)

## Code Patterns to Follow
- Use `authManager.getUserRole()` to check if user is admin
- Show/hide elements based on role: `document.body.className = 'role-admin'`
- Use CSS classes like `.role-admin .add-button { display: block; }`
- Make AJAX calls to `/api/{resource}` endpoints
- Update UI dynamically without page refresh

## Testing Checklist
- [ ] Admin login works
- [ ] Add buttons appear for admin users
- [ ] Forms open and validate input
- [ ] Data saves to database
- [ ] Content displays in interface
- [ ] Edit/delete functions work
- [ ] Viewer mode hides admin features

## Deployment
The user deploys to Manus platform. After making changes:
1. Test locally first
2. User will handle deployment
3. Provide clear instructions for any new dependencies

## Important Notes
- Keep existing authentication system
- Maintain responsive design
- Follow established styling patterns
- Don't break existing functionality
- Focus on user experience and simplicity

## Success Criteria
The user should be able to log in as admin and add research items, deliverables, business processes, AI technologies, software tools, and integration configurations through intuitive forms.

