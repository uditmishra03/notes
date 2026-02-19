servers = [
    {"name": "web-1", "cpu": 75},
    {"name": "db-1", "cpu": 90},
    {"name": "cache-1", "cpu": 60},
    {"name": "web-2", "cpu": 85},
]

servers_sorted = sorted(servers,
                        key = lambda x: x['cpu'],
                        reverse= True)

# print(servers_sorted)

for servers in servers_sorted:
    print(servers['name'])