from collections import defaultdict

logs = [
    {"service": "auth", "level": "ERROR", "host": "h1"},
    {"service": "auth", "level": "ERROR", "host": "h2"},
    {"service": "auth", "level": "INFO",  "host": "h1"},
    {"service": "api",  "level": "ERROR", "host": "h3"},
    {"service": "api",  "level": "ERROR", "host": "h3"},
    {"service": "api",  "level": "WARNING", "host": "h4"},
    {"service": "db",   "level": "ERROR", "host": "h5"},
    {"service": "db",   "level": "ERROR", "host": "h6"},
    {"service": "db",   "level": "ERROR", "host": "h5"},
]



service_log_counter = defaultdict(lambda: {"TOTAL": 0, 
                                  "ERROR": 0,
                                  "Hosts": set()})

for log in logs:
    service = log['service']
    level = log['level']
    host = log['host']

    service_log_counter[service]["TOTAL"] +=1
    if level == "ERROR":
        service_log_counter[service]["ERROR"] +=1
        service_log_counter[service]["Hosts"].add(host)


# print(service_log_counter)

ranked = sorted(service_log_counter.items(), key=lambda x:x[1]["ERROR"], reverse=True)

# print(ranked)

for service, data in ranked:
    print(f"{service} ERROR:{data['ERROR']} HOSTS:{len(data['Hosts'])}")