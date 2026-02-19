services = [
    {"name": "auth", "errors": 5},
    {"name": "db", "errors": 12},
    {"name": "cache", "errors": 3},
    {"name": "api", "errors": 9},
    {"name": "worker", "errors": 12},
]


sorted_services = sorted(services, key=lambda x:x['errors'], reverse=True)

print(sorted_services)

count = 0
error_count_checker = set()
for service in sorted_services[:3]:
    # if count < 3  and service['errors'] not in error_count_checker:
        print(f"{service['name']} {service['errors']}")
        # error_count_checker.add(service['errors'])
        # count +=1
