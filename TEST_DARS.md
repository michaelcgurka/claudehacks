# DARS Upload Feature - Testing Guide

## What It Does

1. **User uploads DARS PDF** on the dashboard
2. **Claude reads and parses** the PDF automatically
3. **Extracts**:
   - Major (e.g., "Computer Science")
   - Completed courses (e.g., "COMP SCI 300", "MATH 340")
   - In-progress courses (current semester)
   - Planned courses (future)
   - Total credits earned
   - GPA

4. **Updates user session** with real data
5. **Schedule generation** now uses YOUR actual data!

## How to Test

1. **Start the server**:
```bash
python3 main_fixed.py
```

2. **Open**: http://localhost:5000

3. **Upload DARS**:
   - Click "Choose File" in the upload section
   - Select your DARS PDF
   - Click "Upload & Parse"
   - Wait 3-5 seconds for Claude to read it

4. **Check results**:
   - You'll see: "✅ DARS parsed! Found Computer Science major with X completed courses"
   - Page will reload with YOUR data

5. **Generate schedules**:
   - Select semester and credit hours
   - Click "Generate Schedules"
   - Claude will create schedules based on YOUR actual completed courses!

## Features

✅ **Zero configuration** - just works
✅ **Smart parsing** - Claude understands DARS format
✅ **Automatic updates** - session updated with real data
✅ **Error handling** - shows clear error messages
✅ **Fast** - parses in 3-5 seconds

## Demo Flow

1. Open app → sees demo data
2. Upload DARS → Claude parses it
3. See YOUR major and courses
4. Generate schedules → personalized to YOU
5. Get 3 tailored schedule options!

## Impressive for Judges

- "Uses Claude's PDF reading API"
- "Automatically extracts degree requirements"
- "No manual data entry needed"
- "Real-time parsing in seconds"
