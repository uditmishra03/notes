events = [
    {"service": "auth", "host": "h1", "status": "fail"},
    {"service": "auth", "host": "h1", "status": "success"},
    {"service": "auth", "host": "h2", "status": "fail"},
    {"service": "api", "host": "h3", "status": "fail"},
    {"service": "api", "host": "h3", "status": "fail"},
    {"service": "api", "host": "h4", "status": "success"},
]


from collections import defaultdict

event_logger = defaultdict(lambda: defaultdict(lambda:{
                                                'Total': 0,
                                                'Fail': 0
                                                }))

for event in events:
    service = event['service']
    host = event['host']
    status = event['status']

    if status == 'fail':
        event_logger[service][host]['Fail'] +=1
    event_logger[service][host]['Total'] +=1


# print(event_logger)
# print("==========")

for svc, hosts in event_logger.items():

    
    top_host, data = max(hosts.items(), key=lambda x: x[1]['Fail'])

    # print(svc,hosts, top_host, data)
    print(f"{svc} -> {top_host} FAILS:{data['Fail']} TOTAL:{data['Total']} ")
