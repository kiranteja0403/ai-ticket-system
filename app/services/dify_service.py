def analyze_issue(issue: str):
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
