# University Course Scheduler

An intelligent course scheduling assistant that uses Claude AI to generate personalized class schedules based on degree requirements, completed courses, and student preferences.

## Features

- **University Authentication**: Mock authentication system with email, password, and Duo 2FA
- **AI-Powered Scheduling**: Uses Claude Sonnet 4.5 to generate intelligent schedule recommendations
- **Multiple Schedule Options**: Provides 3 different schedule approaches (balanced, theory-focused, practical-focused)
- **Prerequisite Checking**: Automatically filters courses based on completed prerequisites
- **Credit Hour Targeting**: Generates schedules that match your desired credit load
- **Clean UI**: Modern, responsive interface for easy navigation

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
SECRET_KEY=your_random_secret_key_here
```

### 3. Run the Application

```bash
python main.py
```

The server will start at http://localhost:5000

## Demo Usage

### Login
- **Email**: Any email address (e.g., `student@university.edu`)
- **Password**: Any password
- **Duo Code**: Any 6-digit number (e.g., `123456`)

### Generate Schedules
1. Select your desired semester
2. Enter target credit hours (6-21)
3. Click "Generate Schedules"
4. Claude will analyze your profile and create 3 personalized schedule options

## Architecture

- **Backend**: Flask web server
- **AI Engine**: Claude Sonnet 4.5 via Anthropic API
- **Frontend**: HTML/CSS/JavaScript (no framework needed)
- **Session Management**: Flask-Session for user authentication
- **Data**: Mock data for courses and degree requirements (easily replaceable with real university APIs)

## Customization for Your University

### Adding Real Course Data

Replace the `COURSES` dictionary in `main.py` with actual course catalog data from your university's API or database.

### Integrating Real Authentication

Replace the `authenticate_user()` and `get_user_profile()` functions with calls to your university's authentication system (e.g., Shibboleth, CAS, LDAP).

### Adding Degree Programs

Extend the `DEGREE_REQUIREMENTS` dictionary with requirements for different majors.

## Future Enhancements

- Real-time course availability checking
- Conflict detection (time slot overlaps)
- Professor ratings integration
- Export schedules to calendar (iCal)
- Save and compare multiple schedules
- Course review integration
- Waitlist management

## Tech Stack

- Python 3.8+
- Flask 3.0
- Anthropic Claude API
- HTML/CSS/JavaScript

## License

MIT License - Built for hackathon
