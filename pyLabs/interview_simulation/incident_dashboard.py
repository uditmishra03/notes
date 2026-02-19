logs = [
    {"service": "auth", "level": "ERROR"},
    {"service": "auth", "level": "INFO"},
    {"service": "auth", "level": "WARNING"},
    {"service": "api", "level": "ERROR"},
    {"service": "api", "level": "ERROR"},
    {"service": "db", "level": "INFO"},
]

service_log_counter = {}

for log in logs:
    service = log['service']
    if service not in service_log_counter:
        service_log_counter[service] = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    
    if log['level'] == "ERROR":
        service_log_counter[service]['ERROR'] +=1

    elif log['level'] == "WARNING":
        service_log_counter[service]['WARNING'] +=1

    elif log['level'] == "INFO":
        service_log_counter[service]['INFO'] +=1

# print(service_log_counter)

for service in service_log_counter:
    print(f"{service} -> ERROR: {service_log_counter[service]['ERROR']} INFO: {service_log_counter[service]['INFO']} WARNING: {service_log_counter[service]['WARNING']}")