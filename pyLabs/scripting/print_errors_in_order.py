errors = {
    "db_error": 5,
    "timeout": 2,
    "disk_full": 8,
    "auth_failed": 3
}

# servers_sorted = sorted(servers,
#                         key = lambda x: x['cpu'],
#                         reverse= True)
# servers_sorted = dict(sorted(unsorted_dict.items(), key=lambda item: item[1], reverse= True))


error_sorted = sorted(errors.items(), key= lambda x: x[1], reverse= True)

print(error_sorted)

for error, count in error_sorted:
    # print(f"{error.key()} {error.value()}")
    print(f"{error} {count}")