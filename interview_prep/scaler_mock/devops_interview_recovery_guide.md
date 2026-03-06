
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

```bash
#!/bin/bash

tasks=$(seq 1 100)

run_task() {
    id=$1
    echo "Starting task $id"
    
    sleep $((RANDOM % 5))

    if [ $((RANDOM % 5)) -eq 0 ]; then
        echo "Task $id failed at $(date)" >> failures.log
    fi
}

for t in $tasks
do
    run_task $t &

    if [[ $(jobs -r | wc -l) -ge 5 ]]
    then
        wait -n
    fi
done

wait
```

---

# Step-by-Step Explanation (Interview Level)

## Step 1 – Background execution

```
run_task $t &
```

This runs each task **asynchronously**.

---

## Step 2 – Check running jobs

```
jobs -r | wc -l
```

This tells how many tasks are running.

Example

```
4 running jobs
```

---

## Step 3 – Enforce concurrency limit

```
if [[ $(jobs -r | wc -l) -ge 5 ]]
```

If running tasks >= 5
we stop launching new tasks.

---

## Step 4 – Wait for slot to free

```
wait -n
```

This waits for **one job to finish** before launching the next.

---

## Step 5 – Final wait

```
wait
```

Ensures script waits for all tasks to finish.

---

# Why This Is a Good Interview Answer

Because it shows

- knowledge of bash job control
- concurrency design
- resource protection
- failure logging

---

# Alternative Solutions (Mention in Interview)

Tools that can solve this easier

### GNU Parallel

```
parallel -j5 run_task ::: {1..100}
```

### xargs

```
seq 100 | xargs -P 5 -I{} run_task {}
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
