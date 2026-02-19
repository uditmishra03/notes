usage = [45, 78, 91, 66, 82, 95, 70]

THRESHOLD = 80

high_usage_count = 0
for each in usage:
    if each > THRESHOLD:
        high_usage_count +=1
        print(f"High usage: {each}")

print(f"Total high usage servers: {high_usage_count}")