# Create a set to track currently banned IPs at the top of main.py
banned_ips = set()

# Inside your loop...
if is_anomalous and ip not in banned_ips:
    if ban_ip(ip):
        banned_ips.add(ip)
        send_slack_alert(...)
