import requests
import json

def send_slack_alert(webhook_url, message):
    payload = {"text": f"🚨 *Anomaly Detected* 🚨\n{message}"}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        return response.status_code == 200
    except Exception as e:
        print(f"Slack error: {e}")
        return False
