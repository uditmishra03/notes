servers = [
    {"name": "web-1", "cpu": 70},
    {"name": "db-1", "cpu": 95},
    {"name": "api-1", "cpu": 88},
]


sorted_servers = sorted(servers, key=lambda x: x['cpu'], reverse= True)

# print(sorted_servers)

print(f"{sorted_servers[0]['name']} {sorted_servers[0]['cpu']}")

# Took 2 mins