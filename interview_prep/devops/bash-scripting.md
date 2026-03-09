# Bash Scripting Interview Questions

---

## 1. Bash Concurrency Worker Pool

### Question
You have a bash script that needs to process **100 tasks**, but only **5 tasks should run at the same time**.
If any task fails, it should be logged.

---

## 2. Background Processes in Bash

When you add `&` after a command, bash runs it **in the background**.

```bash
sleep 10 &
```

This means:
- Shell immediately continues
- Process runs asynchronously

---

## 3. Job Control in Bash

Bash tracks background processes as **jobs**.

```bash
jobs
```

Example output:
```
[1] Running sleep 10 &
[2] Running sleep 5 &
```

Important flags:
- `jobs -r` → show running jobs only
- `jobs -p` → show PIDs

---

## 4. Counting Active Jobs

To control concurrency we count running jobs:

```bash
jobs -r | wc -l
```

| Command | Meaning               |
| ------- | --------------------- |
| jobs -r | show running jobs     |
| wc -l   | count number of lines |

---

## 5. Wait Command

`wait` pauses the script until background jobs finish.

```bash
wait      # Wait for all jobs
wait -n   # Wait for any one job to finish
```

`wait -n` allows **worker pool design**.

---

## 6. Worker Pool Design

### Goal
```
max concurrency = 5
```

### Logic
1. Start task in background
2. Count running jobs
3. If jobs >= 5, wait for one job to finish
4. Continue

---

## 7. Production Style Implementation

### Scenario
You have a file `urls.txt` with 100 URLs. Curl each URL with max 5 concurrent requests. Log failures.

### Script
```bash
#!/bin/bash

URL_FILE="urls.txt"
MAX_CONCURRENT=5

curl_url() {
    url=$1
    echo "Fetching: $url"
    
    curl -sf --connect-timeout 5 --max-time 10 "$url" > /dev/null
    
    if [ $? -ne 0 ]; then
        echo "FAILED: $url at $(date)" >> failures.log
    fi
}

while IFS= read -r url
do
    curl_url "$url" &

    if [[ $(jobs -r | wc -l) -ge $MAX_CONCURRENT ]]
    then
        wait -n
    fi
done < "$URL_FILE"

wait

echo "Done. Check failures.log for any failed URLs."
```

---

## 8. Curl Flags Explained

| Flag                  | Purpose                                 |
| --------------------- | --------------------------------------- |
| `-s`                  | Silent mode (no progress bar)           |
| `-f`                  | Fail silently on HTTP errors (4xx, 5xx) |
| `--connect-timeout 5` | Max 5 seconds to connect                |
| `--max-time 10`       | Max 10 seconds total                    |
| `> /dev/null`         | Discard response body                   |

---

## 9. Exit Code Check

```bash
if [ $? -ne 0 ]; then
```
- `$?` = exit code of last command
- `-ne 0` = not equal to 0 (0 = success)

---

## 10. Reading File Line by Line

```bash
while IFS= read -r url
do
    ...
done < "$URL_FILE"
```

- `IFS=` prevents trimming whitespace
- `-r` prevents backslash escaping
- `< "$URL_FILE"` feeds file as input

---

## 11. Alternative Solutions

### GNU Parallel
```bash
cat urls.txt | parallel -j5 'curl -sf {} || echo "FAILED: {}" >> failures.log'
```

### xargs
```bash
cat urls.txt | xargs -P 5 -I{} sh -c 'curl -sf {} || echo "FAILED: {}" >> failures.log'
```

---

## 12. Zombie Process Cleanup Script

```bash
#!/bin/bash

LOG_FILE="/var/log/zombie_cleanup.log"

echo "=== Zombie cleanup started at $(date) ===" >> "$LOG_FILE"

ZOMBIE_PARENTS=$(ps -eo pid,ppid,state,comm | awk '$3=="Z" {print $2}' | sort -u)

if [ -z "$ZOMBIE_PARENTS" ]; then
    echo "No zombie processes found" >> "$LOG_FILE"
    exit 0
fi

for ppid in $ZOMBIE_PARENTS; do
    SERVICE=$(systemctl status $ppid 2>/dev/null | grep -oP '(?<=─)\S+\.service' | head -1)
    
    if [ -n "$SERVICE" ]; then
        echo "Restarting service: $SERVICE (PPID: $ppid)" >> "$LOG_FILE"
        systemctl restart "$SERVICE"
    else
        echo "Could not identify service for PPID: $ppid" >> "$LOG_FILE"
    fi
done

echo "=== Cleanup completed ===" >> "$LOG_FILE"
```

---

## 13. Associative Arrays for Deduplication

```bash
#!/bin/bash
declare -A RESTARTED_SERVICES

ZOMBIE_PARENTS=$(ps -eo ppid,state | awk '$2=="Z" {print $1}')

for ppid in $ZOMBIE_PARENTS; do
    SERVICE=$(systemctl status $ppid 2>/dev/null | grep -oP '\S+\.service' | head -1)
    
    if [ -n "${RESTARTED_SERVICES[$SERVICE]}" ]; then
        echo "Skipping $SERVICE (already restarted)"
        continue
    fi
    
    systemctl restart "$SERVICE"
    RESTARTED_SERVICES[$SERVICE]=1
    echo "Restarted: $SERVICE"
done
```

---

## 14. Why This Is a Good Interview Answer

Shows:
- Knowledge of bash job control
- Concurrency design
- Resource protection
- Real failure detection using exit codes

---

## 15. Key Interview Points for Bash

1. Zombies can't be killed directly (they're already dead)
2. Only the parent process can clean them up by calling `wait()`
3. Restarting parent service forces cleanup
4. Always deduplicate PIDs to avoid unnecessary restarts
