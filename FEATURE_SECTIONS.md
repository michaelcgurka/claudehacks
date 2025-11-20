# Course Sections Feature

## Overview
Added functionality to fetch and display real-time course sections with meeting times from the UW-Madison API.

## Changes Made

### 1. Backend (main.py)
- **New API Endpoint**: `/api/course-sections/<course_code>`
  - Accepts course code as URL parameter
  - Takes semester as query parameter
  - Returns list of sections with meeting times, instructors, and seat availability

### 2. API Client (uw_api.py)
- **Already implemented**: `get_course_sections()` method
  - Fetches sections for a specific course
  - Returns section details including:
    - Section number and type (LEC, DIS, etc.)
    - Meeting days and times
    - Building and room location
    - Instructor names
    - Seat availability (available/total)

### 3. Frontend (templates/dashboard.html)

#### CSS Additions:
- `.course-item-expanded` - Makes course items clickable with expand/collapse indicators
- `.sections-container` - Container for section listings
- `.section-item` - Individual section display with hover effects
- `.section-header` - Section number and seat availability
- `.section-seats` - Color-coded seat availability badges (green/yellow/red)
- `.section-instructor` - Instructor information display
- `.section-time` - Meeting time and location display

#### JavaScript Additions:
- **toggleSections()** function:
  - Fetches sections when user clicks on a course
  - Caches results to avoid redundant API calls
  - Displays loading states
  - Formats and renders section information
  - Color-codes seat availability:
    - Green: 10+ seats available
    - Yellow: 1-9 seats available
    - Red: No seats available

## User Experience

### How It Works:
1. User generates schedules using the form
2. Recommended schedules are displayed with courses
3. Each course shows a dropdown arrow indicator (▼)
4. Click any course to expand and view available sections
5. Sections show:
   - Section number and type
   - Instructor name
   - Meeting days (e.g., MWF, TR)
   - Meeting times
   - Location (building + room)
   - Real-time seat availability
6. Click again to collapse sections

### Visual Indicators:
- **Expandable courses**: Show arrow indicators (▼/▲)
- **Loading state**: "Loading sections..." message
- **Color-coded seats**:
  - 🟢 Available (10+ seats)
  - 🟡 Limited (1-9 seats)
  - 🔴 Full (0 seats)
- **Hover effects**: Sections highlight on mouse hover

## Technical Notes

### API Integration:
- Uses existing UW-Madison enrollment API
- Fetches real-time data from `https://enroll.wisc.edu/api/search/v1`
- Parses complex course and section data structures

### Performance:
- Lazy loading: Sections only fetched when clicked
- Caching: Once loaded, sections aren't re-fetched
- Smooth animations for expand/collapse

### Error Handling:
- Graceful fallback if API fails
- Clear error messages to user
- Console logging for debugging

## Future Enhancements

Potential improvements:
- Visual calendar/timetable view
- Schedule conflict detection
- Filter sections by time preferences
- Save favorite sections
- Export schedule to calendar format
