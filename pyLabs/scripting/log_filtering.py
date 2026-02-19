logs = [
    "INFO Service started",
    "ERROR Database down",
    "WARNING Disk almost full",
    "ERROR Timeout occurred",
    "INFO Health check passed",
]

error_logs=[]
for log in logs:
    if "ERROR" in log:
        error_logs.append(log)

print(error_logs)