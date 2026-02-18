log_data = """
ERROR Disk failure on node-1
INFO Service restarted successfully
WARNING High memory usage detected
ERROR Disk failure on node-1
INFO Health check passed
ERROR Unable to connect to database
WARNING High memory usage detected
ERROR Disk failure on node-2
"""

log_data = log_data.strip()
# print(log_data)

log_arr = log_data.split()

words= {}

for word in log_arr:
    word= word.lower()
    if word in words:
        words[word] +=1
    else:
        words[word] =1

# print(words)

print(f"error: {words.get('error', 0)}")
# print(f"failure: {words['failure']}")
print(f"failure: {words.get('failure', 0)}")
# print(f"warning: {words['warning']}")
print(f"warning: {words.get('warning', 0)}")