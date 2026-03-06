
# DevOps Interview Recovery Guide
This document converts the mock interview feedback into **actionable interview answers and explanations**.
Goal: move answers from **2/5 → 4–5/5 depth**.

---

<details>
<summary><b>Question 1 – Bash Concurrency Worker Pool</b></summary>

## Interview Question
You have a bash script that needs to process **100 tasks**, but only **5 tasks should run at the same time**.
If any task fails, it should be logged.

Explain:
- approach
- implementation
- concurrency control

---

## Core Concepts Interviewers Expect

## 1. Background Processes in Bash

When you add `&` after a command, bash runs it **in the background**.

Example

```bash
sleep 10 &
```

This means:
- shell immediately continues
- process runs asynchronously

---

## 2. Job Control in Bash

Bash tracks background processes as **jobs**.

Command:

```bash
jobs
```

Example output:

```
[1] Running sleep 10 &
[2] Running sleep 5 &
```

Important flags

```
jobs -r   → show running jobs only
jobs -p   → show PIDs
```

---

## 3. Counting Active Jobs

To control concurrency we count running jobs.

```
jobs -r | wc -l
```

Breakdown:

| Command | Meaning               |
| ------- | --------------------- |
| jobs -r | show running jobs     |
| wc -l   | count number of lines |

So this returns the **number of active background processes**.

Example

```
jobs -r | wc -l
3
```

Meaning 3 jobs are running.

---

## 4. Wait Command

`wait` pauses the script until background jobs finish.

Example

```
wait
```

Wait for **all jobs**.

More useful:

```
wait -n
```

Wait for **any one job to finish**.

This allows **worker pool design**.

---

# Worker Pool Design

Goal

```
max concurrency = 5
```

Logic

1. Start task in background
2. Count running jobs
3. If jobs >= 5
4. Wait for one job to finish

---

# Production Style Implementation

**Scenario:** You have a file `urls.txt` with 100 URLs. Curl each URL with max 5 concurrent requests. Log failures.

**urls.txt example:**
```
https://api.example.com/health
https://api.example.com/users
https://api.example.com/orders
...
```

**Script:**
```bash
#!/bin/bash

URL_FILE="urls.txt"
MAX_CONCURRENT=5

curl_url() {
    url=$1
    echo "Fetching: $url"
    
    # Curl with timeout, silent mode, fail on HTTP errors
    curl -sf --connect-timeout 5 --max-time 10 "$url" > /dev/null
    
    # Check actual exit code
    if [ $? -ne 0 ]; then
        echo "FAILED: $url at $(date)" >> failures.log
    fi
}

# Read URLs from file
while IFS= read -r url
do
    curl_url "$url" &

    # Enforce concurrency limit
    if [[ $(jobs -r | wc -l) -ge $MAX_CONCURRENT ]]
    then
        wait -n
    fi
done < "$URL_FILE"

# Wait for remaining jobs to finish
wait

echo "Done. Check failures.log for any failed URLs."
```

**Curl flags explained:**

| Flag                  | Purpose                                 |
| --------------------- | --------------------------------------- |
| `-s`                  | Silent mode (no progress bar)           |
| `-f`                  | Fail silently on HTTP errors (4xx, 5xx) |
| `--connect-timeout 5` | Max 5 seconds to connect                |
| `--max-time 10`       | Max 10 seconds total                    |
| `> /dev/null`         | Discard response body                   |

**Exit code check:**
```bash
if [ $? -ne 0 ]; then
```
- `$?` = exit code of last command
- `-ne 0` = not equal to 0 (0 = success)
- Logs actual failures, not simulated ones

---

# Step-by-Step Explanation (Interview Level)

## Step 1 – Read URLs from file

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

## Step 2 – Background execution

```bash
curl_url "$url" &
```

The `&` runs each curl **asynchronously** in the background.

---

## Step 3 – Check running jobs

```bash
jobs -r | wc -l
```

This tells how many curl requests are currently running.

---

## Step 4 – Enforce concurrency limit

```bash
if [[ $(jobs -r | wc -l) -ge $MAX_CONCURRENT ]]
```

If running jobs >= 5, we pause before launching more.

---

## Step 5 – Wait for slot to free

```bash
wait -n
```

This waits for **one job to finish** before launching the next.

---

## Step 6 – Final wait

```bash
wait
```

Ensures script waits for all remaining curl requests to finish.

---

## Step 7 – Real failure logging

```bash
if [ $? -ne 0 ]; then
    echo "FAILED: $url at $(date)" >> failures.log
fi
```

- `$?` captures the **actual exit code** of curl
- Non-zero exit code = real failure (network error, timeout, HTTP 4xx/5xx)
- Logs the URL that failed, not just a random simulation

---

# Why This Is a Good Interview Answer

Because it shows

- knowledge of bash job control
- concurrency design
- resource protection
- **real failure detection** using exit codes

---

# Alternative Solutions (Mention in Interview)

Tools that can solve this easier

### GNU Parallel

```bash
cat urls.txt | parallel -j5 'curl -sf {} || echo "FAILED: {}" >> failures.log'
```

### xargs

```bash
cat urls.txt | xargs -P 5 -I{} sh -c 'curl -sf {} || echo "FAILED: {}" >> failures.log'
```

ALTERNATE VERSION:
```
URL_FILE="urls"

while IFS = read -r url
do
(
    curl -sf $url > /dev/null
    if [ $? -ne 0 ]; then
    echo "Failed : $url at $(date)" >> failure.log
    fi
)&

if [ $(jobs -r | wc -l) -ge 5 ]; then
    wait -n
fi

done > "$URL_FILE"

wait

echo "Completed all url execution"

```

Mentioning alternatives shows **engineering maturity**.

</details>

---

<details>
<summary><b>Question 2 – Docker Network Isolation</b></summary>

## Interview Question

Multiple containers are running on a host.
One container should **not see network traffic of another container**.

How would you design network isolation?

---

# Docker Networking Internals

Each container has:

```
Network namespace
Virtual ethernet pair (veth)
Linux bridge
```

Flow

```
Container
   |
veth pair
   |
docker0 bridge
   |
Host network
```

Bridge behaves like a **switch / hub**.

Meaning containers on same bridge may observe traffic.

---

# Isolation Strategies

## 1 Custom Bridge Networks

```
docker network create mynet
```

Containers in different bridges cannot communicate unless allowed.

---

## 2 Macvlan Network

Gives container its **own MAC address**.

```
docker network create -d macvlan
```

Benefits

- L2 isolation
- appears as real device on network

---

## 3 Overlay Network

Used in

```
Docker Swarm
Kubernetes
```

Allows multi-host container networking.

---

## 4 Host Network

```
--network host
```

Container shares host stack.

Not isolated.

---

# Ideal Interview Answer

Best isolation approach

```
macvlan network
or
separate bridge networks
```

Combine with

```
iptables
network policies
```

</details>

---

<details>
<summary><b>Question 3 – Kubernetes DNS Debugging</b></summary>

## Interview Question

Pods cannot resolve service names inside cluster.

Example

```
curl my-service
```

fails.

How do you troubleshoot?

---

# DNS Flow in Kubernetes

```
Pod
 ↓
CoreDNS
 ↓
Kubernetes API
 ↓
Service endpoints
```

---

# Step-by-Step Debugging

## Step 1 – Verify CoreDNS

```
kubectl get pods -n kube-system
```

---

## Step 2 – Test DNS inside cluster

```
kubectl run busybox --image=busybox -it --rm -- nslookup kubernetes.default
```

---

## Step 3 – Inspect CoreDNS config

```
kubectl edit configmap coredns -n kube-system
```

Check plugins

```
forward
kubernetes
cache
```

---

## Step 4 – Check Service

```
kubectl get svc kube-dns -n kube-system
```

---

## Step 5 – Network Policies

Ensure DNS port allowed

```
UDP 53
TCP 53
```

</details>

---

<details>
<summary><b>Prometheus Storage Internals</b></summary>

Prometheus stores data in **TSDB**.

Structure

```
WAL
 ↓
Head block
 ↓
Block files
 ↓
Compaction
```

---

## WAL

Write Ahead Log.

Temporary storage before commit.

Prevents data loss.

---

## Blocks

Prometheus stores metrics in

```
2 hour block segments
```

---

## Compaction

Small blocks merge into bigger blocks.

Reduces disk fragmentation.

---

## Retention

Controlled via flag

```
--storage.tsdb.retention.time
```

Example

```
--storage.tsdb.retention.time=15d
```

</details>

---

<details>
<summary><b>Observability Pipeline</b></summary>

Typical architecture

```
Application
 ↓
Prometheus
 ↓
Alertmanager
 ↓
PagerDuty / Slack
```

Metrics Types

- Counter
- Gauge
- Histogram
- Summary

</details>

---

<details>
<summary><b>Structured Debugging Framework</b></summary>

Always answer debugging questions using layered analysis

```
Application
↓
Container
↓
Kubernetes
↓
Network
↓
Cloud infrastructure
```

Example

Slow API

Step 1 → app logs

Step 2 → container CPU

Step 3 → pod restarts

Step 4 → network latency

Step 5 → cloud load balancer metrics

</details>

---

<details>
<summary><b>AWS Networking Debugging</b></summary>

Debug order

```
Client
↓
ALB
↓
Target group
↓
EC2 / Pod
↓
VPC routing
↓
Security group
↓
NACL
```

Tools

```
VPC Flow Logs
CloudWatch metrics
ELB access logs
```

</details>

---

<details>
<summary><b>Multi Account AWS Security</b></summary>

Secure architecture

```
Account A
     |
PrivateLink
     |
Account B
```

Alternative

```
Transit Gateway
```

Security layers

```
IAM
Resource policies
Endpoint policies
Security groups
```

</details>

---

<details>
<summary><b>Key Interview Strategy</b></summary>

Every answer should include

1 Problem understanding  
2 Architecture explanation  
3 Implementation steps  
4 Failure scenarios  
5 Tradeoffs

Example

“First I would verify if the issue is DNS or network related.
Then I would validate CoreDNS pods.
Next I would run nslookup from inside cluster….”

This structured thinking is what interviewers score highly.

</details>

---

# End of Guide
