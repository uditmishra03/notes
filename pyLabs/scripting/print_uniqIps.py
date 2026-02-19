ips = [
    "10.0.0.1",
    "192.168.1.10",
    "10.0.0.1",
    "172.16.0.5",
    "192.168.1.10",
]


# print(ips)

# print(set(ips))

uniq_ip=[]
seen = set()
for ip in ips:
    # print(ip)
    if ip not in seen:
        seen.add(ip)
        uniq_ip.append(ip)

print(uniq_ip)
# print(seen)