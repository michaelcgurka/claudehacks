"""
Quick test script to demonstrate the UW-Madison API integration.
Run this to see real course data!
"""

from uw_api import UWMadisonAPI

def test_api():
    print("Testing UW-Madison Course API...\n")

    api = UWMadisonAPI()

    # Test 1: Get CS courses for Spring 2026
    print("=== Computer Science Courses (Spring 2026) ===")
    cs_courses = api.get_courses(term="Spring 2026", subject="COMP SCI")

    print(f"Found {len(cs_courses)} CS courses\n")

    # Show first 5
    for course in cs_courses[:5]:
        print(f"{course['code']}: {course['name']}")
        print(f"   Credits: {course['credits']}")
        print(f"   Prereqs: {course['prereqs']}")
        print()

    # Test 2: Get MATH courses
    print("\n=== Math Courses (Spring 2026) ===")
    math_courses = api.get_courses(term="Spring 2026", subject="MATH")

    print(f"Found {len(math_courses)} MATH courses\n")

    for course in math_courses[:3]:
        print(f"{course['code']}: {course['name']} ({course['credits']} credits)")

    print("\n✅ API Integration Working!")
    print(f"Total courses fetched: {len(cs_courses) + len(math_courses)}")

if __name__ == "__main__":
    test_api()
