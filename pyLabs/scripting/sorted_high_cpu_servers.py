servers = [
    {"name": "web-1", "cpu": 70},
    {"name": "db-1", "cpu": 95},
    {"name": "cache-1", "cpu": 60},
    {"name": "web-2", "cpu": 88},
    {"name": "web-3", "cpu": 99}
]

THRESHOLD = 80

high_cpu_usage_servers = []

# Filter first
for server in servers:
    if server['cpu'] > THRESHOLD: 
        high_cpu_usage_servers.append(server)

# print(high_cpu_usage_servers)
# Sort by cpu
high_cpu_usage_servers= sorted(high_cpu_usage_servers, key= lambda x: x['cpu'], reverse= True)


# display results
# print(high_cpu_usage_servers)
for server in high_cpu_usage_servers:
    print(f"{server['name']} {server['cpu']}")