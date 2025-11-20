# Quick Start Guide - 5 Minutes to Demo!

## Setup

1. **Install dependencies**:
```bash
pip3 install flask anthropic python-dotenv requests flask-session
```

2. **Create .env file**:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > .env
echo "SECRET_KEY=hackathon2024" >> .env
```

3. **Run the server**:
```bash
python3 main.py
```

4. **Open browser**: http://localhost:5000

## Demo Flow

1. **Login Page**:
   - Email: any email
   - Password: any password
   - Duo: `123456`

2. **Dashboard**:
   - Select semester (Spring 2026, Fall 2025, etc.)
   - Enter credit hours (12-18)
   - Click "Generate Schedules"

3. **AI Magic**:
   - Claude analyzes degree requirements
   - Generates 3 personalized schedule options
   - Each with rationale and course details

## What It Does

- ✅ Authentic UW-Madison UI
- ✅ Real course data structure (mock for now, API ready)
- ✅ Claude AI schedule generation
- ✅ Prerequisite awareness
- ✅ Multiple schedule approaches

## Next Steps (Post-Hackathon)

- Connect real UW API (code ready in `uw_api.py`)
- Parse DARS reports for actual degree requirements
- Add time conflict detection
- Export to Google Calendar
