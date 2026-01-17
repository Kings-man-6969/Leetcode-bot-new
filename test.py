import os
import json
import requests
from dotenv import load_dotenv

# Load .env file
load_dotenv()

LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
CSRFTOKEN = os.getenv("CSRFTOKEN")

if not LEETCODE_SESSION or not CSRFTOKEN:
    raise ValueError("LEETCODE_SESSION and CSRFTOKEN must be set in .env!")

# Cookies and headers
cookies = {
    "LEETCODE_SESSION": LEETCODE_SESSION.strip(),
    "csrftoken": CSRFTOKEN.strip()
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-csrftoken": CSRFTOKEN.strip()
}

# Problem details
PROBLEM_SLUG = "majority-element"
QUESTION_ID = "169"
SOLUTION_CODE = """class Solution:
    def majorityElement(self, nums):
        count = 0
        candidate = None
        for num in nums:
            if count == 0:
                candidate = num
            count += (1 if num == candidate else -1)
        return candidate
"""

# Test login
def test_login():
    url = "https://leetcode.com/api/problems/all/"
    r = requests.get(url, cookies=cookies, headers=headers)
    if r.status_code == 200 and "user_name" in r.text:
        print("✅ Cookies are valid! Logged in.")
        return True
    else:
        print("❌ Cookies invalid or expired!")
        return False

# Submit solution
def submit_solution():
    test_login()
    submit_url = f"https://leetcode.com/problems/{PROBLEM_SLUG}/submit/"
    payload = {
        "lang": "python3",
        "question_id": QUESTION_ID,
        "typed_code": SOLUTION_CODE
    }
    r = requests.post(submit_url, json=payload, cookies=cookies, headers=headers)
    if r.status_code == 200 and "submission_id" in r.text:
        submission_id = json.loads(r.text).get("submission_id")
        print(f"✅ Submission sent! Submission ID: {submission_id}")
    else:
        print("❌ Submission failed. Check cookies or session.")

# Main
if __name__ == "__main__":
    submit_solution()
