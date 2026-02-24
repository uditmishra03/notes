from collections import defaultdict

log_level_counter = defaultdict(int)
app_log = "app.log"

error_count = 0

with open(app_log) as file:
    for line in file:
        log_level = line.split()[0]
        # print(log_level)
        if log_level not in log_level_counter:
            log_level_counter[log_level] = log_level_counter.get(log_level, 0)+1
        else:
            log_level_counter[log_level] +=1

for level,count in log_level_counter.items():
    print(f"{level}: {count}")
    