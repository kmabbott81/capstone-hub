# AI Collaboration Guide - Enhanced Capstone Hub

## Project Overview
This is Kyle Mabbott's HL Stearns AI Strategy capstone project management system. A comprehensive web application for managing research, experiments, deliverables, and business process analysis.

## Current Status
- **Live URL**: https://77h9ikc6780p.manus.space
- **Admin Password**: `HLStearns2025!`
- **Status**: Fully functional with authentication system
- **Last Updated**: September 2025

## Architecture

### Backend (Flask)
- **Framework**: Flask with SQLAlchemy
- **Database**: SQLite (app.db)
- **API Structure**: RESTful endpoints under `/api/`
- **Authentication**: Client-side localStorage with admin/viewer roles

### Frontend (Vanilla JS/HTML/CSS)
- **Framework**: Pure JavaScript (no frameworks)
- **Styling**: Custom CSS with responsive design
- **Charts**: Chart.js for data visualization
- **Authentication**: Client-side role management

## Key Features Implemented

### 1. Authentication System
- **File**: `src/static/auth-fixed.js`
- **Admin Password**: `HLStearns2025!`
- **Roles**: admin (full access), viewer (read-only)
- **Status Indicator**: Small badge in bottom right when logged in

### 2. Main Sections
1. **Dashboard** - Project overview with metrics
2. **Deliverables Timeline** - Course milestones and deadlines
3. **Business Processes** - HL Stearns process evaluation
4. **AI Technologies** - Comprehensive AI tool catalog
5. **Software & Tech Stack** - Tool evaluation matrix
6. **Research Management** - Primary/secondary research tracking
7. **Integrations** - Third-party platform connections

### 3. Data Models
Located in `src/models/`:
- `deliverable.py` - Project deliverables and milestones
- `business_process.py` - Business process analysis
- `ai_technology.py` - AI tools and platforms
- `software_tool.py` - Software evaluation
- `research_item.py` - Research documentation
- `integration.py` - Third-party integrations

### 4. API Routes
Located in `src/routes/`:
- `deliverables.py` - CRUD for deliverables
- `business_processes.py` - Process management
- `ai_technologies.py` - AI tool management
- `software_tools.py` - Software tool management
- `research_items.py` - Research item management
- `integrations.py` - Integration management
- `advanced_features.py` - Analytics and exports

## Current Issues to Address

### 1. Missing Add/Edit Functionality
**Problem**: Admin users can't see add/edit buttons
**Solution Needed**: 
- Add "Add New" buttons to each section when admin is logged in
- Create modal forms for adding content
- Implement edit/delete buttons for existing items

### 2. Content Creation Forms
**Needed Features**:
- Text input fields
- Image upload capability
- Link management for cloud folders/databases
- Rich text editing
- File attachment support

## Development Priorities

### Immediate (High Priority)
1. **Add Content Creation UI**
   - Add buttons visible only to admin users
   - Modal forms for each content type
   - Form validation and submission

2. **Implement CRUD Operations**
   - Connect frontend forms to backend API
   - Add edit/delete functionality
   - Real-time updates without page refresh

3. **File Upload System**
   - Image upload and display
   - Document attachment
   - Cloud storage integration

### Medium Priority
1. **Enhanced Research Management**
   - Question templates
   - Research methodology tracking
   - Citation management

2. **Integration Improvements**
   - Notion API integration
   - Google Drive/Sheets connection
   - Microsoft 365 integration

3. **Analytics Dashboard**
   - Progress tracking
   - ROI calculations
   - Timeline visualization

### Future Enhancements
1. **Export Functionality**
   - PDF report generation
   - Excel export
   - Presentation slides

2. **Collaboration Features**
   - Comments system
   - Version control
   - Sharing capabilities

## File Structure
```
capstone-hub-complete-dev-package/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── models/                 # Database models
│   ├── routes/                 # API endpoints
│   └── static/                 # Frontend files
│       ├── index.html          # Main application
│       ├── styles.css          # Main styling
│       ├── banner-killer.css   # Authentication styling
│       ├── auth-fixed.js       # Authentication logic
│       └── app.js              # Main application logic
├── requirements.txt            # Python dependencies
└── README.md                   # Basic setup instructions
```

## Setup Instructions for AI Agents

### 1. Environment Setup
```bash
cd capstone-hub-complete-dev-package
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Development Server
```bash
cd src
python main.py
```
Application will be available at `http://localhost:5000`

### 3. Database Initialization
Database is automatically created on first run using SQLAlchemy.

## API Documentation

### Authentication
- No server-side authentication required
- Client-side role management via localStorage
- Admin password: `HLStearns2025!`

### Endpoints
All endpoints follow RESTful conventions:
- `GET /api/{resource}` - List all items
- `POST /api/{resource}` - Create new item
- `GET /api/{resource}/{id}` - Get specific item
- `PUT /api/{resource}/{id}` - Update item
- `DELETE /api/{resource}/{id}` - Delete item

### Resources
- `/api/deliverables` - Project deliverables
- `/api/business-processes` - Business processes
- `/api/ai-technologies` - AI technologies
- `/api/software-tools` - Software tools
- `/api/research-items` - Research items
- `/api/integrations` - Third-party integrations

## Styling Guidelines

### Color Scheme
- Primary: #667eea (purple-blue gradient)
- Secondary: #764ba2 (purple)
- Success: #4CAF50 (green)
- Warning: #FF9800 (orange)
- Danger: #f44336 (red)

### Design Principles
- Clean, professional interface
- Responsive design (mobile-friendly)
- Consistent spacing and typography
- Subtle shadows and gradients
- Color-coded sections and status indicators

## Testing
- Manual testing via browser
- Admin login functionality
- All navigation sections
- Responsive design on different screen sizes

## Deployment
- Currently deployed on Manus platform
- Can be deployed to any Flask-compatible hosting
- Static files served directly by Flask
- SQLite database (can be upgraded to PostgreSQL for production)

## Next Steps for AI Agents

1. **Implement Add/Edit UI**: Create modal forms and buttons
2. **Connect Frontend to Backend**: Wire up API calls
3. **Add File Upload**: Implement image and document upload
4. **Enhance User Experience**: Add loading states, error handling
5. **Expand Functionality**: Add more content types and features

## Contact Information
- **Project Owner**: Kyle Mabbott
- **Institution**: OEMBA 2025
- **Company**: HL Stearns
- **Project**: AI Strategy Capstone

## Important Notes for AI Agents
- Maintain the existing authentication system
- Keep the clean, professional design aesthetic
- Ensure mobile responsiveness
- Follow the established API patterns
- Test thoroughly before deployment
- Document any new features added

