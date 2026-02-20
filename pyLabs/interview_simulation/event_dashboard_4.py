events = [
    {"service": "auth", "host": "h1", "status": "fail"},
    {"service": "auth", "host": "h1", "status": "fail"},
    {"service": "auth", "host": "h2", "status": "fail"},
    {"service": "api", "host": "h3", "status": "fail"},
    {"service": "api", "host": "h3", "status": "fail"},
    {"service": "api", "host": "h4", "status": "fail"},
    {"service": "db", "host": "h5", "status": "fail"},
]

from collections import defaultdict

event_logger = defaultdict(lambda: defaultdict(int))

for event in events:
    service = event['service']
    host = event['host']
    status = event['status']

    if status == 'fail':
        event_logger[service][host] +=1
    
# print(event_logger)

for svc, hosts in event_logger.items():
    
    top_host, fail_count = max(hosts.items(), key=lambda x: x[1])
    print(f"{svc} -> {top_host} FAILS:{fail_count}")