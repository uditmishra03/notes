processes = [
    {"name": "nginx", "status": "running"},
    {"name": "redis", "status": "stopped"},
    {"name": "mysql", "status": "running"},
    {"name": "api", "status": "stopped"},
]


for each in processes:
    # print(f"{each['name']} {each['status']}")
    if each['status'] == 'stopped':
        print(f"Stopped: {each['name']}")