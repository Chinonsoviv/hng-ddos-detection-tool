import time
from blocker import unban_ip

def auto_unban_logic(banned_ips, notifier, webhook):
    # This is a simplified version for your main loop to call
    now = time.time()
    for ip, ban_time in list(banned_ips.items()):
        if now - ban_time > 600: # 10 minutes (first backoff)
            if unban_ip(ip):
                del banned_ips[ip]
                notifier(webhook, f"Unbanned {ip} after 10 mins")
