import os
import subprocess
import tempfile
from google import genai

# ---------- CONFIG ----------
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

USER_STORY = """
As a user, I want to log in with valid credentials
so that I can access my dashboard.
"""

# ---------- STEP 1: Generate Test Cases ----------
def generate_test_cases(user_story):
    model = "models/gemini-1.5-flash"
    prompt = f"You are a senior QA. Generate test cases for: {user_story}"
    response = client.models.generate_content(model=model, contents=prompt)
    return response.text

# ---------- STEP 2: Convert to Playwright ----------
def convert_to_playwright(test_cases):
    model = "models/gemini-1.5-flash"
    prompt = f"Convert these to Playwright Python async code. Output ONLY code: {test_cases}"
    response = client.models.generate_content(model=model, contents=prompt)
    # Clean markdown if present
    return response.text.replace("```python", "").replace("```", "").strip()

# ---------- STEP 3: SELF-HEALING ENGINE ----------
def fix_code_with_ai(bad_code, error_message):
    prompt = f"Fix this Playwright code.\nERROR: {error_message}\nCODE: {bad_code}\nReturn ONLY fixed code."
    response = client.models.generate_content(model="models/gemini-1.5-flash", contents=prompt)
    return response.text.replace("```python", "").replace("```", "").strip()

def execute_and_fix(initial_code, max_attempts=3):
    current_code = initial_code
    for attempt in range(max_attempts):
        print(f"--- Execution Attempt {attempt + 1} ---")
        
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as f:
            f.write(current_code)
            temp_path = f.name

        # Runs pytest on the generated file
        result = subprocess.run(["pytest", temp_path], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Success! The script ran perfectly.")
            return current_code
        else:
            print("❌ Execution failed. Asking Gemini to fix it...")
            error_log = result.stderr + result.stdout
            current_code = fix_code_with_ai(current_code, error_log)
            
    return current_code

# ---------- RUN EVERYTHING ----------
if __name__ == "__main__":
    print("1. Generating test cases...")
    test_cases = generate_test_cases(USER_STORY)

    print("2. Generating initial Playwright code...")
    raw_code = convert_to_playwright(test_cases)

    print("3. Starting Self-Healing Execution...")
    final_verified_code = execute_and_fix(raw_code)
    
    print("\n--- FINAL VERIFIED CODE ---")
    print(final_verified_code)