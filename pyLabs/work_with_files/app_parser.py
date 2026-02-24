
# log_file = "app.log"

# with open(log_file) as file:
#     for line in file:
#         print(line.strip())
        
# # for line in log_file:
# #     print(line)

import time

log_file = "app.log"

with open(log_file) as file:
    file.seek(0, 2)   # move to end of file

    while True:
        line = file.readline()

        if not line:
            time.sleep(1)
            continue

        print(line.strip())