
# ---------- CONFIG ----------

import os
from google import genai

# ---------- CONFIG ----------

from google import genai
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

for m in client.models.list():
    print(m.name)

# ---------- INPUT ----------
USER_STORY = """
As a user, I want to log in with valid credentials
so that I can access my dashboard.
"""

# ---------- STEP 1: GEMINI - Generate Test Cases ----------
def generate_test_cases(user_story):
    model = "models/gemini-flash-latest"   # FIXED MODEL NAME

    prompt = f"""
    You are a senior QA engineer.
    Generate detailed test cases from the following user story.
    Include positive and negative scenarios.
    Format output as numbered steps with expected results.
    URL- https://rahulshettyacademy.com/loginpagePractise/
    UserName-   rahulshettyacademy
    Password-   learning
  

    User Story:
    {user_story}
    """

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text

# ---------- STEP 2: GEMINI - Convert to Playwright ----------
def convert_to_playwright(test_cases):
    # Using System Instructions for better role-playing
    config = {
        "system_instruction": "You are an expert QA Automation Engineer. Output ONLY raw Python code using Playwright async and pytest. No explanations."
    }
    
    prompt = f"""
    Convert these test cases into a Playwright script for: https://rahulshettyacademy.com/loginpagePractise/
    
    Test Cases:
    {test_cases}
    """

    response = client.models.generate_content(
        model="gemini-flash-latest", # Updated to a stable version
        config=config,
        contents=prompt
    )

    return response.text

# ---------- RUN ----------
if __name__ == "__main__":
    print("Generating test cases...\n")
    test_cases = generate_test_cases(USER_STORY)
    print(test_cases)

    print("\nGenerating Playwright code...\n")
    playwright_code = convert_to_playwright(test_cases)
    print(playwright_code)