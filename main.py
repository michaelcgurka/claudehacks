import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import anthropic
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Mock course data - replace with actual university API integration
COURSES = {
    "CS": [
        {"code": "CS101", "name": "Intro to Computer Science", "credits": 3, "prereqs": []},
        {"code": "CS201", "name": "Data Structures", "credits": 3, "prereqs": ["CS101"]},
        {"code": "CS301", "name": "Algorithms", "credits": 3, "prereqs": ["CS201"]},
        {"code": "CS202", "name": "Computer Architecture", "credits": 3, "prereqs": ["CS101"]},
        {"code": "CS305", "name": "Database Systems", "credits": 3, "prereqs": ["CS201"]},
        {"code": "CS310", "name": "Operating Systems", "credits": 3, "prereqs": ["CS202"]},
    ],
    "MATH": [
        {"code": "MATH101", "name": "Calculus I", "credits": 4, "prereqs": []},
        {"code": "MATH102", "name": "Calculus II", "credits": 4, "prereqs": ["MATH101"]},
        {"code": "MATH201", "name": "Linear Algebra", "credits": 3, "prereqs": ["MATH101"]},
        {"code": "MATH301", "name": "Discrete Mathematics", "credits": 3, "prereqs": ["MATH101"]},
    ],
    "ENG": [
        {"code": "ENG101", "name": "English Composition I", "credits": 3, "prereqs": []},
        {"code": "ENG102", "name": "English Composition II", "credits": 3, "prereqs": ["ENG101"]},
    ]
}

# Mock degree requirements
DEGREE_REQUIREMENTS = {
    "Computer Science": {
        "required_courses": ["CS101", "CS201", "CS301", "CS202", "MATH101", "MATH102", "MATH201", "ENG101"],
        "elective_categories": {
            "CS_electives": {"required": 2, "options": ["CS305", "CS310"]},
            "MATH_electives": {"required": 1, "options": ["MATH301"]}
        },
        "total_credits": 120
    }
}


@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        duo_code = data.get('duo_code')

        # Mock authentication - replace with actual university authentication
        if email and password and duo_code:
            # In production, validate against university API
            if authenticate_user(email, password, duo_code):
                user_data = get_user_profile(email)
                session['user'] = user_data
                return jsonify({"success": True, "message": "Login successful"})
            else:
                return jsonify({"success": False, "message": "Invalid credentials"}), 401

        return jsonify({"success": False, "message": "Missing credentials"}), 400

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/api/generate-schedules', methods=['POST'])
def generate_schedules():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    credit_hours = data.get('credit_hours', 15)
    semester = data.get('semester', 'Fall 2025')

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


def authenticate_user(email, password, duo_code):
    """
    Mock authentication function.
    Replace with actual university authentication API integration.
    """
    # For hackathon demo, accept any credentials with 6-digit duo code
    return len(duo_code) == 6 and duo_code.isdigit()


def get_user_profile(email):
    """
    Mock function to retrieve user profile.
    Replace with actual university API call.
    """
    # Mock student data
    return {
        "email": email,
        "name": email.split('@')[0].title(),
        "major": "Computer Science",
        "year": "Junior",
        "completed_courses": ["CS101", "CS201", "MATH101", "ENG101"],
        "gpa": 3.5
    }


def generate_schedule_with_claude(major, completed_courses, target_credits, semester):
    """
    Use Claude to generate intelligent schedule recommendations.
    """
    degree_reqs = DEGREE_REQUIREMENTS.get(major, {})

    # Build available courses (courses where prereqs are met)
    available_courses = []
    for dept, courses in COURSES.items():
        for course in courses:
            if course['code'] not in completed_courses:
                prereqs_met = all(prereq in completed_courses for prereq in course['prereqs'])
                if prereqs_met:
                    available_courses.append(course)

    # Create prompt for Claude
    prompt = f"""You are a university course scheduling advisor. Generate 3 different recommended schedules for a {major} student.

Student Information:
- Major: {major}
- Completed Courses: {', '.join(completed_courses)}
- Target Credit Hours: {target_credits}
- Semester: {semester}

Degree Requirements:
{json.dumps(degree_reqs, indent=2)}

Available Courses (prerequisites met):
{json.dumps(available_courses, indent=2)}

Generate 3 diverse schedule options that:
1. Meet the target credit hours (±2 credits is acceptable)
2. Progress toward degree requirements
3. Consider course difficulty balance
4. Provide different focuses (e.g., theory-heavy, practical-heavy, balanced)

Return your response as a JSON array of schedules. Each schedule should have:
- "name": A descriptive name for the schedule approach
- "courses": Array of course codes
- "total_credits": Total credit hours
- "rationale": Brief explanation of why this schedule makes sense

Example format:
[
  {{
    "name": "Balanced Core Focus",
    "courses": ["CS202", "MATH102", "ENG102"],
    "total_credits": 10,
    "rationale": "Balances core CS requirements with math and communication skills"
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
                for dept, courses in COURSES.items():
                    for course in courses:
                        if course['code'] == course_code:
                            schedule['course_details'].append(course)
                            break

        return schedules

    except Exception as e:
        print(f"Error generating schedules: {e}")
        # Fallback to simple schedule
        return [{
            "name": "Default Schedule",
            "courses": [c['code'] for c in available_courses[:4]],
            "total_credits": sum(c['credits'] for c in available_courses[:4]),
            "course_details": available_courses[:4],
            "rationale": "Basic schedule based on available courses"
        }]


if __name__ == '__main__':
    app.run(debug=True, port=5000)
