import time
import threading
import yaml
import statistics
import psutil
from flask import Flask, render_template_string
from monitor import TrafficMonitor
from baseline import BaselineManager
from detector import check_anomaly
from notifier import send_slack_alert
from blocker import ban_ip

# 1. SETUP
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

monitor = TrafficMonitor(config['log_path'])
baseline = BaselineManager()
banned_ips_list = []
start_time = time.time()

# 2. DASHBOARD LOGIC (Live Metrics UI)
app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>HNG Anomaly Detector Dashboard</title>
    <meta http-equiv="refresh" content="3">
    <style>
        body { font-family: sans-serif; background: #f4f4f9; padding: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        h1 { color: #333; }
        .metric { font-size: 24px; font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <h1>Cloud.ng Anomaly Detection Engine</h1>
    <div class="grid">
        <div class="card"><h3>Global Req/s</h3><p class="metric">{{ req_s }}</p></div>
        <div class="card"><h3>Effective Mean</h3><p class="metric">{{ mean }}</p></div>
        <div class="card"><h3>Std Dev</h3><p class="metric">{{ stddev }}</p></div>
        <div class="card"><h3>CPU Usage</h3><p class="metric">{{ cpu }}%</p></div>
    </div>
    <div class="card">
        <h3>Banned IPs</h3>
        <ul>
            {% for ip in banned %}
                <li><code>{{ ip }}</code></li>
            {% else %}
                <li>No active bans</li>
            {% endfor %}
        </ul>
    </div>
    <p>Uptime: {{ uptime }} seconds</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        DASHBOARD_HTML,
        req_s=len(monitor.global_window),
        mean=round(baseline.mean, 2),
        stddev=round(baseline.stddev, 2),
        cpu=psutil.cpu_percent(),
        banned=banned_ips_list,
        uptime=int(time.time() - start_time)
    )

# 3. ENGINE LOGIC
def baseline_updater():
    while True:
        time.sleep(60)
        rates = monitor.get_rates()
        baseline.update_history(rates['global'])
        baseline.recalculate()

def detector_loop():
    print("Starting Detection Engine...")
    threading.Thread(target=monitor.tail_logs, daemon=True).start()
    while True:
        time.sleep(2)
        rates = monitor.get_rates()
        for ip, rate in rates['ips'].items():
            if ip in banned_ips_list: continue
            
            is_anomalous, reason = check_anomaly(rate, baseline.mean, baseline.stddev)
            if is_anomalous:
                if ban_ip(ip):
                    banned_ips_list.append(ip)
                    send_slack_alert(config['slack']['webhook_url'], f"Banned {ip}. Rate: {rate}/s. Reason: {reason}")

if __name__ == '__main__':
    # Start Dashboard in background
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()
    # Start Baseline and Detector
    threading.Thread(target=baseline_updater, daemon=True).start()
    detector_loop()
