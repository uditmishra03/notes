usage_logs = [
    {"server": "web-1", "cpu": 85},
    {"server": "db-1", "cpu": 92},
    {"server": "cache-1", "cpu": 65},
    {"server": "web-2", "cpu": 88},
]

THRESHOLD = 80
high_cpu_server_count = 0
for log in usage_logs:
    if log['cpu'] >=THRESHOLD:
        high_cpu_server_count +=1
        print(f"High CPU: {log['server']}")


print(f"Total high CPU servers: {high_cpu_server_count}")