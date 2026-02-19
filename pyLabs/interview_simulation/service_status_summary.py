services = [
    {"name": "auth", "status": "up"},
    {"name": "db", "status": "down"},
    {"name": "cache", "status": "up"},
    {"name": "api", "status": "down"},
    {"name": "api", "status": "down"},
    {"name": "api-2", "status": "down"},
    {"name": "api-4", "status": "down"},
    {"name": "api-5", "status": "down"},
    {"name": "cache", "status": "up"},
    {"name": "cache", "status": "up"},
    {"name": "cache", "status": "up"}
]

up_svc_counter, down_svc_counter = 0, 0

for service in services:
    if service['status'] == 'up':
        up_svc_counter +=1
    elif service['status'] == 'down':
        down_svc_counter +=1


print(f"up : {up_svc_counter}")
print(f"down : {down_svc_counter}")

# Took 4 mins