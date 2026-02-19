services = [
    {"name": "auth", "status": "up", "cpu": 72},
    {"name": "db", "status": "down", "cpu": 95},
    {"name": "cache", "status": "up", "cpu": 88},
    {"name": "api", "status": "down", "cpu": 91},
    {"name": "worker", "status": "up", "cpu": 65},
    {"name": "search", "status": "up", "cpu": 93},
]

sorted_service = sorted(services, key=lambda x:x['cpu'], reverse=True)

# print(sorted_service)

THRESHOLD = 90
down_service_count = 0
for service in sorted_service:
    if service['status'] == 'down' or service['cpu'] > THRESHOLD:
        down_service_count +=1
        print(f"ALERT: {service['name']} {service['status']} {service['cpu']}")

print("========")
print(f"Total alerts: {down_service_count}")