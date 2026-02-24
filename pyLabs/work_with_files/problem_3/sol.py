from collections import defaultdict

log_file = "app.log"


log_level_counter = defaultdict(int)

with open(log_file) as file:
    for line in file:
        parts = line.strip().split()
        # if not parts:
        #     continue
        log_level = parts[0].upper()
        # print(line)
        # print(log_level)
        log_level_counter[log_level] =log_level_counter.get(log_level, 0)+1


# print(log_level_counter)

for log_level, count in log_level_counter.items():
    print(f"{log_level}: {count}")