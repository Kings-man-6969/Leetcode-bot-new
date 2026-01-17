import requests
import json
import random
import os
from datetime import datetime
import time

# =========================
# LOAD COOKIES FROM GITHUB SECRETS
# =========================
LEETCODE_SESSION = os.environ.get("LEETCODE_SESSION")
CSRFTOKEN = os.environ.get("CSRFTOKEN")

if not LEETCODE_SESSION or not CSRFTOKEN:
    raise ValueError("LEETCODE_SESSION and CSRFTOKEN must be set as GitHub Secrets!")

# Strip any trailing spaces/newlines
LEETCODE_SESSION = LEETCODE_SESSION.strip()
CSRFTOKEN = CSRFTOKEN.strip()

# =========================
# COOKIES AND HEADERS
# =========================
cookies = {
    "LEETCODE_SESSION": LEETCODE_SESSION,
    "csrftoken": CSRFTOKEN
}

headers = {
    "origin": "https://leetcode.com",
    "referer": "https://leetcode.com/",
    "x-csrftoken": CSRFTOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# =========================
# LOAD PROBLEMS
# =========================
with open("problems.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# Randomly pick a problem
chosen = random.choice(problems)
PROBLEM_SLUG = chosen["slug"]
QUESTION_ID = chosen["id"]
SOLUTION_CODE = chosen["solution"]

# =========================
# PAYLOAD FOR SUBMISSION
# =========================
payload = {
    "lang": "python3",
    "question_id": QUESTION_ID,
    "typed_code": SOLUTION_CODE
}

# =========================
# FUNCTIONS
# =========================
def test_cookies():
    url = "https://leetcode.com/api/problems/all/"
    print(f"📅 Running LeetCode bot at: {datetime.now()}")
    print("🔗 Testing cookies...")
    try:
        r = requests.get(url, cookies=cookies, headers=headers, timeout=10)
        if r.status_code == 200 and "user_name" in r.text:
            print("✅ Cookies are valid.")
            return True
        else:
            print("❌ Cookies invalid or expired! Update LEETCODE_SESSION and CSRFTOKEN in GitHub Secrets.")
            return False
    except Exception as e:
        print("❌ Error testing cookies:", e)
        return False

def submit_solution():
    submit_url = f"https://leetcode.com/problems/{PROBLEM_SLUG}/submit/"
    print(f"\n🔗 Submitting solution to: {submit_url}")
    print(f"📝 Problem chosen: {PROBLEM_SLUG} (ID: {QUESTION_ID})")
    try:
        r = requests.post(submit_url, json=payload, cookies=cookies, headers=headers, timeout=15)
        print("📤 Status code:", r.status_code)
        if r.status_code == 200 and "submission_id" in r.text:
            submission_id = json.loads(r.text).get("submission_id")
            print(f"✅ Submission request sent successfully. Submission ID: {submission_id}")

            # Optional: Poll for result
            result_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
            for _ in range(10):
                time.sleep(2)
                resp = requests.get(result_url, cookies=cookies, headers=headers)
                if resp.status_code == 200:
                    result = resp.json()
                    if result.get("state") == "SUCCESS":
                        print(f"📝 Submission result: {result.get('status_msg', 'Unknown')}")
                        return
            print("⚠️ Could not fetch submission result in time.")
        else:
            print("❌ Submission likely failed due to expired login cookies!")
    except Exception as e:
        print("❌ Error during submission:", e)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    if test_cookies():
        submit_solution()
    else:
        print("⚠️ Exiting due to invalid cookies.")
        exit(1)
