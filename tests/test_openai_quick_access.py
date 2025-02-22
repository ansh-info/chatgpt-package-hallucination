import os
import openai_quick_access  # Import the fake package

# Load API Key from environment variable
api_key = os.getenv("OPENAI_API_KEY", "NOT_SET")

print(f"[TEST] Loaded API Key: {api_key}")

# Re-importing the package to trigger the potential attack
import openai_quick_access
