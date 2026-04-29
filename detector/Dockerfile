FROM python:3.9-slim
# This line installs the missing iptables tool
RUN apt-get update && apt-get install -y iptables && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
