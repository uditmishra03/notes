logs = [
    "ERROR Disk full",
    "INFO Service started",
    "ERROR Timeout",
    "WARNING Memory high",
    "ERROR DB connection failed",
]

error_counter = 0
for log in logs:
    if 'ERROR' in log:
        error_counter +=1

print(f"Total ERROR logs: {error_counter}")


## completed in 2-3 mins
