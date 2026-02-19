logs = [
    {"service": "auth", "level": "ERROR"},
    {"service": "auth", "level": "ERROR"},
    {"service": "auth", "level": "INFO"},
    {"service": "api", "level": "ERROR"},
    {"service": "api", "level": "WARNING"},
    {"service": "db", "level": "ERROR"},
    {"service": "db", "level": "ERROR"},
    {"service": "db", "level": "ERROR"},
]

service_error_count = {}
service_all_count = {}

for log in logs:
    service = log['service']
    level = log['level']
    if level == 'ERROR':
        service_error_count[service] = service_error_count.get(service, 0)+1
    service_all_count[service] = service_all_count.get(service, 0)+1


# print(service_all_count)
# print(service_error_count)

for service in service_all_count:
    print(f"{service} ERROR:{service_error_count.get(service, 0)} TOTAL:{service_all_count.get(service, 0)}")