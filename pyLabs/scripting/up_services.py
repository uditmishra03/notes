services = [
    {"name": "auth", "status": "up"},
    {"name": "db", "status": "down"},
    {"name": "cache", "status": "up"},
    {"name": "api", "status": "down"},
]

up_services = []

for service in services:
    if service['status'] == 'up':
        up_services.append(service['name'])

# up_services = [
#     s["name"]
#     for s in services
#     if s["status"] == "up"
# ]


print(up_services)