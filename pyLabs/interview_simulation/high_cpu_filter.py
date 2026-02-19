servers = [
    {"name": "web-1", "cpu": 70},
    {"name": "db-1", "cpu": 95},
    {"name": "cache-1", "cpu": 60},
    {"name": "api-1", "cpu": 88},
]

sorted_servers = sorted(servers, key=lambda x:x['cpu'], reverse= True)

# print(sorted_servers)
THRESHOLD = 80
for server in sorted_servers:
    if server['cpu'] > THRESHOLD:
        print(f"{server['name']}")


# Took 4 mins.