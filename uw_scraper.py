import requests
from bs4 import BeautifulSoup
import time
import re
from typing import Dict, List, Optional
import json


class UWMadisonScraper:
    """
    Web scraper for University of Wisconsin-Madison student portal.
    Simplified version for hackathon demo - uses session cookies.
    """

    def __init__(self, cookies_dict: Optional[Dict] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })

        if cookies_dict:
            self.session.cookies.update(cookies_dict)

        self.authenticated = False
        self.netid = None
        self.base_url = "https://public.enroll.wisc.edu"

    def authenticate(self, netid: str, password: str, duo_code: str) -> bool:
        """
        Authenticate with UW-Madison portal using NetID, password, and Duo.

        Args:
            netid: Student NetID
            password: Student password
            duo_code: 6-digit Duo code from mobile app

        Returns:
            bool: True if authentication successful
        """
        try:
            # Step 1: Initial login page
            login_url = "https://my.wisc.edu/"
            response = self.session.get(login_url)

            # Step 2: Submit NetID and password
            # TODO: Need to inspect the actual form fields from login page
            login_data = {
                'j_username': netid,
                'j_password': password,
                '_eventId_proceed': 'Log In'
            }

            # Find the actual login form action URL
            soup = BeautifulSoup(response.text, 'html.parser')
            login_form = soup.find('form')
            if login_form:
                action_url = login_form.get('action')
                if not action_url.startswith('http'):
                    action_url = 'https://login.wisc.edu' + action_url

                # Submit credentials
                response = self.session.post(action_url, data=login_data, allow_redirects=True)

            # Step 3: Handle Duo authentication
            # The Duo page shows a code that user enters in their app
            # We need to wait for user to approve the push notification
            # For automation, we'll implement duo_code submission

            soup = BeautifulSoup(response.text, 'html.parser')

            # Check if we're on Duo page
            if 'duosecurity.com' in response.url or 'duo' in response.text.lower():
                # TODO: Implement Duo bypass or automation
                # For now, this requires manual intervention or Duo API integration
                print("Duo authentication detected. Manual approval needed.")
                # In production, you'd use duo_client library or selenium
                pass

            # Step 4: Verify authentication success
            # Check if we can access MyUW Home
            home_response = self.session.get('https://my.wisc.edu/')

            if 'MyUW Home' in home_response.text or 'Course Search' in home_response.text:
                self.authenticated = True
                self.netid = netid
                return True

            return False

        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def get_available_courses(self, term: str = "Spring 2026") -> List[Dict]:
        """
        Scrape available courses for a given term.

        Args:
            term: Semester term (e.g., "Spring 2026", "Fall 2025")

        Returns:
            List of course dictionaries
        """
        if not self.authenticated:
            raise Exception("Must authenticate first")

        courses = []

        try:
            # TODO: Navigate to Course Search & Enroll
            # Need actual URL - waiting for screenshot
            search_url = "https://PUBLIC.enroll.wisc.edu/search"  # Placeholder

            # TODO: Implement actual search logic once we see the page structure
            # This is a placeholder implementation

            return courses

        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []

    def get_student_transcript(self) -> List[str]:
        """
        Get list of completed courses from student transcript.

        Returns:
            List of course codes (e.g., ["CS101", "MATH101"])
        """
        if not self.authenticated:
            raise Exception("Must authenticate first")

        completed_courses = []

        try:
            # TODO: Navigate to transcript page
            # Need actual URL and page structure
            pass

        except Exception as e:
            print(f"Error fetching transcript: {e}")

        return completed_courses

    def get_dars_report(self) -> Dict:
        """
        Parse DARS (Degree Audit Reporting System) report.

        Returns:
            Dictionary with degree requirements and progress
        """
        if not self.authenticated:
            raise Exception("Must authenticate first")

        dars_data = {
            "major": "",
            "required_courses": [],
            "completed_courses": [],
            "remaining_requirements": [],
            "total_credits": 0,
            "completed_credits": 0
        }

        try:
            # TODO: Navigate to DARS report
            # Need actual URL and page structure
            pass

        except Exception as e:
            print(f"Error fetching DARS report: {e}")

        return dars_data

    def search_courses(self, subject: str = "", keywords: str = "") -> List[Dict]:
        """
        Search for specific courses by subject or keywords.

        Args:
            subject: Subject code (e.g., "CS", "MATH")
            keywords: Search keywords

        Returns:
            List of matching courses
        """
        # TODO: Implement course search
        return []


# Helper function to convert term names
def parse_term(term_string: str) -> str:
    """
    Convert term string to UW-Madison term code.
    Example: "Spring 2026" -> "1262"
    """
    season_codes = {
        "Spring": "2",
        "Summer": "3",
        "Fall": "4"
    }

    # Extract season and year
    parts = term_string.split()
    if len(parts) == 2:
        season = parts[0]
        year = parts[1][-2:]  # Last 2 digits

        if season in season_codes:
            return "1" + year + season_codes[season]

    return ""
