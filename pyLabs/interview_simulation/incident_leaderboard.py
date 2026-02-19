logs = [
    {"service": "auth", "level": "ERROR"},
    {"service": "api", "level": "ERROR"},
    {"service": "auth", "level": "ERROR"},
    {"service": "cache", "level": "WARNING"},
    {"service": "api", "level": "ERROR"},
    {"service": "db", "level": "ERROR"},
    {"service": "db", "level": "ERROR"},
]

service_error_count = {}

for log in logs:

    if log['level'] == 'ERROR':
        service = log['service']
        level = log['level']
        service_error_count[service] = service_error_count.get(service, 0) +1


sorted_svc_error_count = sorted(service_error_count.items(), key=lambda x:x[1], reverse=True)

# print(sorted_svc_error_count)
for service, error_count in sorted_svc_error_count[:2]:
    print(service, error_count)