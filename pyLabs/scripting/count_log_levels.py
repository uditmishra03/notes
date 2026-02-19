logs = [
    "ERROR Disk full",
    "INFO Service started",
    "ERROR Database down",
    "WARNING Memory high",
    "INFO Health check",
    "ERROR Timeout",
    "ERROR Memory full",
    "WARNING Memory high",
    "WARNING Memory high"
]


log_level_dict = {}

for log in logs:
    # print(log.split()[0])
    level = log.split()[0]
    log_level_dict[level] = log_level_dict.get(level, 0) +1

sorted_log_levels= sorted(log_level_dict.items(), key=lambda x: x[1], reverse= True)

# print(sorted_log_levels)

for level,count in sorted_log_levels:
    print(f"{level} {count}")