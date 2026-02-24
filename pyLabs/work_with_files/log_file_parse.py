from collections import defaultdict


error_count = 0
log = []
with open('log.txt') as f:
    for line in f:
        # print((line.strip()))
        data=line.strip()
        log.append(data)
        if 'ERROR' in data:
            error_count +=1

print("ERROR Count:", error_count)
        # log.append(data)

# with open('log.txt') as file:
#     data = file.read()


# print(data, type(data))

print(log)

# print(data.split())
