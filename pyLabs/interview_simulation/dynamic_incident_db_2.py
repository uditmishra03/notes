from collections import defaultdict

logs = [
    {"service": "auth", "level": "ERROR"},
    {"service": "auth", "level": "INFO"},
    {"service": "auth", "level": "WARNING"},
    {"service": "api", "level": "ERROR"},
    {"service": "api", "level": "ERROR"},
    {"service": "db", "level": "INFO"},
    {"service": "db", "level": "DEBUG"},
    {"service": "fe", "level": "FAILED"},
    {"service": "be", "level": "INFO"},
]

svc_log_counter = defaultdict(lambda: defaultdict(int))

for log in logs:
    service = log['service']
    level = log['level']

    svc_log_counter[service][level] +=1


print(svc_log_counter)
for svc, levels in svc_log_counter.items():
    # print(svc, levels)
    parts = []
    for level, count in levels.items():
        parts.append(f"{level}:{count}")
    
    # print(parts)
    
    print(f"{svc} -> " + " ".join(parts))