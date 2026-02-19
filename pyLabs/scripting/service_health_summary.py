services = [
    {"name": "auth", "status": "up"},
    {"name": "db", "status": "down"},
    {"name": "cache", "status": "up"},
    {"name": "api", "status": "down"},
    {"name": "worker", "status": "up"},
]

up_count, down_count = 0, 0

for service in services:
    if service['status'] == 'up':
        up_count +=1
    elif service['status'] == 'down':
        down_count +=1

print(f"UP: {up_count}\nDOWN: {down_count}")