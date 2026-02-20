from collections import defaultdict

events = [
    {"service": "auth", "status": "fail", "host": "h1"},
    {"service": "auth", "status": "fail", "host": "h1"},
    {"service": "auth", "status": "success", "host": "h2"},
    {"service": "api", "status": "fail", "host": "h3"},
    {"service": "api", "status": "fail", "host": "h4"},
    {"service": "db", "status": "success", "host": "h5"},
]


event_logger = defaultdict(lambda: {
                            "Total": 0, 
                            "Fail": 0,
                })

for event in events:
    service = event['service']
    status = event['status']

    event_logger[service]["Total"] +=1
    if status == "fail":
        event_logger[service]["Fail"] +=1
    
# event_logger[service]['FailRate'] = round(event_logger[service]["Fail"]/event_logger[service]["Total"],2)


# print(event_logger)

for svc, data in event_logger.items():
    fail_rate= round(data['Fail']/data['Total'] if data['Total']> 0 else 0,2)
    print(f"{svc} TOTAL:{data['Total']} FAIL:{data['Fail']} RATE:{fail_rate}")

