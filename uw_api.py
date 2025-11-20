"""
UW-Madison Course API Client
Uses the public course search API to fetch real course data.
"""

import requests
from typing import Dict, List


class UWMadisonAPI:
    """Client for UW-Madison public course search API."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        })
        # Try the authenticated endpoint first (requires login)
        self.api_url = "https://enroll.wisc.edu/api/search/v1"

    def get_courses(self, term: str = "Spring 2026", subject: str = "") -> List[Dict]:
        """
        Fetch courses from UW-Madison API.

        Args:
            term: Semester (e.g., "Spring 2026", "Fall 2025")
            subject: Subject code (e.g., "comp sci", "math")

        Returns:
            List of course dicts
        """
        try:
            term_code = self._parse_term(term)

            # The exact parameters that work in the browser
            params = {
                "termCode": term_code,
                "term": term_code,
                "keywords": subject.lower(),  # Lowercase seems to work better
                "openSeats": "ALL"
            }

            # Try the exact endpoint structure
            response = self.session.get(f"{self.api_url}/courses", params=params)
            response.raise_for_status()

            data = response.json()
            courses = []

            for hit in data.get("hits", []):
                courses.append({
                    "code": hit.get("courseDesignationRaw", ""),
                    "name": hit.get("title", ""),
                    "credits": hit.get("creditRange", "3"),
                    "min_credits": hit.get("minimumCredits", 3),
                    "max_credits": hit.get("maximumCredits", 3),
                    "prereqs": hit.get("enrollmentPrerequisites", "None"),
                    "description": hit.get("description", ""),
                    "subject": hit.get("subject", {}).get("shortDescription", "")
                })

            return courses

        except Exception as e:
            print(f"API Error: {e}")
            return []

    def _parse_term(self, term: str) -> str:
        """Convert 'Spring 2026' to '1262'."""
        seasons = {"Spring": "2", "Summer": "3", "Fall": "4"}

        parts = term.split()
        if len(parts) == 2:
            season, year = parts
            if season in seasons:
                return "1" + year[-2:] + seasons[season]

        return "1262"  # Default Spring 2026
