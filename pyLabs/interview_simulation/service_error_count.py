logs = [
    {"service": "auth", "level": "ERROR", "message": "DB timeout"},
    {"service": "api", "level": "INFO", "message": "Request completed"},
    {"service": "auth", "level": "ERROR", "message": "DB timeout"},
    {"service": "cache", "level": "WARNING", "message": "Memory high"},
    {"service": "api", "level": "ERROR", "message": "Timeout"},
    {"service": "auth", "level": "INFO", "message": "Health check"},
    {"service": "api", "level": "ERROR", "message": "Timeout"},
    {"service": "api", "level": "ERROR", "message": "Timeout"},
    {"service": "api", "level": "ERROR", "message": "Timeout"},
]

service_error_count = {}

for log in logs:
    if log['level'] == 'ERROR':
        service = log['service']
        service_error_count[service] = service_error_count.get(service, 0) +1

# print(service_error_count)

sorted_service_error_count =dict(sorted(service_error_count.items(), key=lambda x: x[1], reverse= True))

# print(sorted_service_error_count)

THRESHOLD = 1
for service, error_count in sorted_service_error_count.items():
    if error_count > THRESHOLD:
        print(f"ALERT {service} {error_count}") 