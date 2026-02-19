servers = [
    {"name": "web-1", "cpu": 70},
    {"name": "db-1", "cpu": 95},
    {"name": "cache-1", "cpu": 60},
    {"name": "web-2", "cpu": 88},
    {"name": "api-1", "cpu": 91},
]


# for server in servers: 
#     print(server)

# Sort servers by cpu

sorted_servers = sorted(servers, key= lambda x: x['cpu'], reverse= True)

# print(sorted_servers)

for server in sorted_servers[:2]:
    print(f"{server['name']} {server['cpu']}")