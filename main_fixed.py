# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import anthropic
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Mock UW-Madison course data (fallback when API doesn't work)
MOCK_UW_COURSES = [
    {"code": "COMP SCI 200", "name": "Programming I", "credits": 3, "prereqs": "None"},
    {"code": "COMP SCI 300", "name": "Programming II", "credits": 3, "prereqs": "COMP SCI 200"},
    {"code": "COMP SCI 400", "name": "Programming III", "credits": 3, "prereqs": "COMP SCI 300"},
    {"code": "COMP SCI 354", "name": "Machine Organization", "credits": 3, "prereqs": "COMP SCI 300"},
    {"code": "COMP SCI 577", "name": "Algorithms", "credits": 3, "prereqs": "COMP SCI 400"},
    {"code": "COMP SCI 540", "name": "Intro to AI", "credits": 3, "prereqs": "COMP SCI 400"},
    {"code": "COMP SCI 564", "name": "Database Systems", "credits": 3, "prereqs": "COMP SCI 400"},
    {"code": "COMP SCI 536", "name": "Compiler Design", "credits": 3, "prereqs": "COMP SCI 354, COMP SCI 400"},
    {"code": "MATH 340", "name": "Linear Algebra", "credits": 3, "prereqs": "MATH 222"},
    {"code": "MATH 341", "name": "Multivariable Calc", "credits": 4, "prereqs": "MATH 222"},
    {"code": "MATH 431", "name": "Probability", "credits": 3, "prereqs": "MATH 222"},
]

DEGREE_REQUIREMENTS = {
    "Computer Science": {
        "required_courses": ["COMP SCI 200", "COMP SCI 300", "COMP SCI 400", "COMP SCI 354", "COMP SCI 577"],
        "elective_categories": {
            "CS_electives": {"required": 3, "options": ["COMP SCI 540", "COMP SCI 564", "COMP SCI 536"]},
            "MATH_electives": {"required": 2, "options": ["MATH 340", "MATH 341", "MATH 431"]}
        },
        "total_credits": 120
    }
}


@app.route('/')
def index():
    # Auto-login as demo user (skip authentication)
    if 'user' not in session:
        session['user'] = {
            "email": "demo@wisc.edu",
            "name": "Demo Student",
            "major": "Computer Science",
            "year": "Junior",
            "completed_courses": ["COMP SCI 200", "COMP SCI 300", "MATH 221", "MATH 222"],
            "gpa": 3.5
        }
    return render_template('dashboard.html', user=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Skip login - redirect to dashboard
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/api/generate-schedules', methods=['POST'])
def generate_schedules():
    if 'user' not in session:
        # Auto-create user if missing
        session['user'] = {
            "major": "Computer Science",
            "completed_courses": ["COMP SCI 200", "COMP SCI 300", "MATH 221", "MATH 222"]
        }

    data = request.json
    credit_hours = data.get('credit_hours', 15)
    semester = data.get('semester', 'Spring 2026')

    user = session['user']
    major = user.get('major', 'Computer Science')
    completed_courses = user.get('completed_courses', [])

    # Generate schedule recommendations using Claude
    schedules = generate_schedule_with_claude(
        major=major,
        completed_courses=completed_courses,
        target_credits=credit_hours,
        semester=semester
    )

    return jsonify({"schedules": schedules})


def generate_schedule_with_claude(major, completed_courses, target_credits, semester):
    """
    Use Claude to generate intelligent schedule recommendations.
    Uses mock data for reliable demo.
    """
    degree_reqs = DEGREE_REQUIREMENTS.get(major, {})

    # Filter available courses
    available_courses = []
    for course in MOCK_UW_COURSES:
        if course['code'] not in completed_courses:
            available_courses.append(course)

    # Limit to reasonable number for Claude
    available_courses = available_courses[:15]

    # Create prompt for Claude
    prompt = f"""You are a university course scheduling advisor for UW-Madison. Generate 3 different recommended schedules for a {major} student.

Student Information:
- Major: {major}
- Completed Courses: {', '.join(completed_courses)}
- Target Credit Hours: {target_credits}
- Semester: {semester}

Degree Requirements:
{json.dumps(degree_reqs, indent=2)}

Available Courses:
{json.dumps(available_courses, indent=2)}

Generate 3 diverse schedule options that:
1. Meet the target credit hours (±2 credits is acceptable)
2. Progress toward degree requirements
3. Consider course difficulty balance
4. Provide different focuses (e.g., theory-heavy, practical-heavy, balanced)

Return your response as a JSON array of schedules. Each schedule should have:
- "name": A descriptive name for the schedule approach
- "courses": Array of course codes (e.g., ["COMP SCI 400", "MATH 340"])
- "total_credits": Total credit hours
- "rationale": Brief explanation of why this schedule makes sense

Example format:
[
  {{
    "name": "Balanced Core Focus",
    "courses": ["COMP SCI 400", "COMP SCI 354", "MATH 340"],
    "total_credits": 9,
    "rationale": "Balances core CS requirements with essential math foundations"
  }}
]

Return ONLY the JSON array, no other text."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse JSON response
        schedules = json.loads(response_text)

        # Enrich with full course details
        for schedule in schedules:
            schedule['course_details'] = []
            for course_code in schedule['courses']:
                for course in MOCK_UW_COURSES:
                    if course['code'] == course_code:
                        schedule['course_details'].append(course)
                        break

        return schedules

    except Exception as e:
        print(f"Error generating schedules: {e}")
        # Fallback schedule
        return [{
            "name": "Default Schedule",
            "courses": [c['code'] for c in available_courses[:4]],
            "total_credits": sum(c['credits'] for c in available_courses[:4]),
            "course_details": available_courses[:4],
            "rationale": "Basic schedule based on available courses and prerequisites"
        }]


if __name__ == '__main__':
    app.run(debug=True, port=5000)
