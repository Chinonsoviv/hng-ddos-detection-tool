import json
import time
import subprocess
from collections import deque

class TrafficMonitor:
    def __init__(self, log_path):
        self.log_path = log_path
        # Deque for global requests (last 60s)
        self.global_window = deque()
        # Dictionary of deques for per-IP requests
        self.ip_windows = {}

    def tail_logs(self):
        # Using subprocess to tail -F (follows even if log rotates)
        proc = subprocess.Popen(['tail', '-F', self.log_path], stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if not line:
                continue
            
            try:
                entry = json.loads(line.decode('utf-8'))
                self.process_entry(entry)
            except Exception as e:
                print(f"Error parsing log: {e}")

    def process_entry(self, entry):
        now = time.time()
        ip = entry['source_ip']
        
        # Add to global window
        self.global_window.append(now)
        
        # Add to per-IP window
        if ip not in self.ip_windows:
            self.ip_windows[ip] = deque()
        self.ip_windows[ip].append(now)

        # Eviction logic: remove timestamps older than 60s
        self.cleanup(now)

    def cleanup(self, now):
        cutoff = now - 60
        while self.global_window and self.global_window[0] < cutoff:
            self.global_window.popleft()
            
        for ip in list(self.ip_windows.keys()):
            while self.ip_windows[ip] and self.ip_windows[ip][0] < cutoff:
                self.ip_windows[ip].popleft()
            if not self.ip_windows[ip]:
                del self.ip_windows[ip]

    def get_rates(self):
        return {
            "global": len(self.global_window),
            "ips": {ip: len(win) for ip, win in self.ip_windows.items()}
        }
