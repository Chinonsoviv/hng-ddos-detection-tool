# HNG Cloud.ng Anomaly Detection Engine

## Deployment Details
- **Server IP:** 63.176.93.246
- **Metrics Dashboard:** http://63.176.93.246:5000
- **Nextcloud Instance:** http://63.176.93.246

## Architecture
This tool is a Python-based daemon that monitors Nginx JSON logs in real-time. It uses a **sliding window** approach with `collections.deque` to track request rates and calculates a **rolling baseline** (Mean/StdDev) every 60 seconds.

## How it Works
- **Sliding Window:** Tracks requests over the last 60 seconds. When a new request arrives, timestamps older than 60s are evicted.
- **Anomaly Detection:** An IP is blocked via `iptables` if its rate exceeds a Z-score of 3.0 or 5x the baseline mean.
- **Auto-Unban:** Implements a backoff schedule (10m, 30m, 2h).

## Setup Instructions
1. Clone the repo: `git clone <repo-url>`
2. Run the stack: `docker-compose up -d --build`
3. Access the dashboard on port 5000.

## Blog Post
https://dev.to/chinonsoviv/how-i-built-a-real-time-anomaly-detection-engine-for-cloud-storage-2m1f
