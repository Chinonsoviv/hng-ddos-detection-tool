import subprocess

def ban_ip(ip):
    try:
        # Check if the IP is already banned to avoid the "Bad rule" error
        check = subprocess.run(['iptables', '-C', 'DOCKER-USER', '-s', ip, '-j', 'DROP'], capture_output=True)
        if check.returncode == 0:
            return True # Already banned, treat as success

        # If not banned, add the rule
        subprocess.run(['iptables', '-I', 'DOCKER-USER', '-s', ip, '-j', 'DROP'], check=True)
        return True
    except Exception as e:
        print(f"Error banning {ip}: {e}")
        return False
