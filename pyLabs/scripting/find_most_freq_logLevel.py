logs = [
    "ERROR Disk full",
    "INFO Service started",
    "ERROR Database down",
    "WARNING Memory high",
    "INFO Health check",
    "ERROR Timeout",
    "WARNING CPU high",
    "INFO Health check",
    "INFO Health check",
    "INFO Health check"
]

log_counter = {}
for log in logs:
    level = log.split()[0]
    log_counter[level] = log_counter.get(level, 0) +1

# print(log_counter)

log_counter_sorted = sorted(log_counter.items(), key=lambda x:x[1], reverse=True)

print(log_counter_sorted)
# for level, count in log_counter_sorted:
#     print(f"{level} {count}")
level, count = log_counter_sorted[0]
print(f"Most frequent: {level} {count}")