import os
import requests
from dotenv import load_dotenv

load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL")

def analyze_issue(issue: str):
    try:
        url = f"{DIFY_BASE_URL}/chat-messages"
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {},
            "query": f"Classify this support issue and give troubleshooting steps: {issue}",
            "response_mode": "blocking",
            "user": "ticket-system-user"
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        answer = data.get("answer", "")

        return {
            "category": "AI Generated",
            "troubleshooting": answer
        }

    except Exception:
        issue_lower = issue.lower()

        if "wifi" in issue_lower or "network" in issue_lower:
            return {
                "category": "Network Issue",
                "troubleshooting": "Restart router, reconnect WiFi, check network adapter settings."
            }
        elif "slow" in issue_lower or "performance" in issue_lower:
            return {
                "category": "Performance Issue",
                "troubleshooting": "Close background apps, restart system, check disk and memory usage."
            }
        else:
            return {
                "category": "General Issue",
                "troubleshooting": "Please check system settings and contact support if issue continues."
            }
