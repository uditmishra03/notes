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

svc_log_counter= {}

for log in logs:
    service = log['service']
    level = log['level']

    # print(service, level)
    # Check if service exist in dict, if not add
    if service not in svc_log_counter:
        svc_log_counter[service] = {}

        # Check if level exist in dict[service], if not then add
    if level not in svc_log_counter[service]:
        svc_log_counter[service][level] = 0

    svc_log_counter[service][level] +=1

print(svc_log_counter)

for svc, levels in svc_log_counter.items():
    # print(svc, levels)
    parts = []
    for level, count in levels.items():
        parts.append(f"{level}:{count}")
    
    print(parts)
    
    print(f"{svc} -> " + " ".join(parts))
