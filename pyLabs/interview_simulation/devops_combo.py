services = [
    {"name": "auth", "status": "up", "errors": 2},
    {"name": "db", "status": "down", "errors": 10},
    {"name": "cache", "status": "up", "errors": 1},
    {"name": "api", "status": "down", "errors": 5},
]

sorted_services = sorted(services, key=lambda x:x['errors'], reverse= True)

# print(sorted_services)

for service in sorted_services:
    if service['status'] == 'down' or service['errors'] > 5:
        print(f"{service['name']} {service['errors']}")


# Took 3 mins