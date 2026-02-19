logs = [
    "INFO User login success",
    "ERROR Database connection failed",
    "WARNING Disk usage high",
    "ERROR Timeout while calling API",
    "INFO Health check passed",
    "ERROR Database connection failed",
]

count = {}

for line in logs:
    level=line.split()[0]
    print(level)
    if level in count:
        count[level] = count.get(level, 0) +1
    else:
        count[level] =1


print(count)
