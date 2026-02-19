from collections import defaultdict


events = [
    {"service": "auth", "status": "success", "host": "h1"},
    {"service": "auth", "status": "fail", "host": "h1"},
    {"service": "auth", "status": "fail", "host": "h2"},
    {"service": "api", "status": "success", "host": "h3"},
    {"service": "api", "status": "fail", "host": "h3"},
    {"service": "db", "status": "fail", "host": "h4"},
    {"service": "db", "status": "fail", "host": "h5"},
]

event_log_counter = defaultdict(lambda:{
    'Total': 0,
    'Fail': 0,
    'Hosts': set()
})

for event in events:
    svc = event['service']
    status = event['status']
    host = event['host']
    
    event_log_counter[svc]['Total'] +=1
    if status == 'fail':
        event_log_counter[svc]['Fail'] +=1
        event_log_counter[svc]['Hosts'].add(host)


# print(event_log_counter)

# Perform sorting  by Total

ranked_events = sorted(event_log_counter.items(), key=lambda x:x[1]['Total'], reverse= True)

# print(ranked_events)

for svc, data in ranked_events:
    print(f"{svc} → TOTAL:{data['Total']} FAIL:{data['Fail']} HOSTS:{len(data['Hosts'])}")