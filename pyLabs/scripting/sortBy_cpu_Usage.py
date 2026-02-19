servers = [
    {"name": "web-1", "cpu": 75},
    {"name": "db-1", "cpu": 90},
    {"name": "cache-1", "cpu": 60},
    {"name": "web-2", "cpu": 85},
]
# print(servers_sorted)

sorted_list=[]
unsorted_dict= {}
for i in range(len(servers)):
    # print(f"{i}: {servers[i]}")
    # print(f"{servers[i]['name']}: {servers[i]['cpu']}")
    unsorted_dict[servers[i]['name']] = servers[i]['cpu']


# print(unsorted_dict)

# servers_sorted= sorted(unsorted_dict.items(), key=lambda x: x[1])

servers_sorted = dict(sorted(unsorted_dict.items(), key=lambda item: item[1], reverse= True))

for each in servers_sorted.keys():
    print(each)

