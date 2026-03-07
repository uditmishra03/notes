# DevOps Mock Interview -- Question & Answer Reference

This document summarizes the key questions and structured answers from
the DevOps mock interview session.\
It is designed as a quick revision guide.

------------------------------------------------------------------------

<details>
<summary><b>1. Bash Script to Handle Zombie Processes</b></summary>

## Question

How would you write a bash script to scan for zombie processes, find
their parent PIDs, and restart the parent service?

## Understanding Zombie Processes

A **zombie process** (also called a defunct process) is a process that has completed execution but still has an entry in the process table. This happens when:

1. Child process terminates
2. Parent process has NOT yet called `wait()` to read its exit status
3. The process entry remains in the process table with state `Z`

**Why zombies are problematic:**
- Each zombie consumes a PID (process ID)
- System has limited PIDs (usually 32768 by default)
- Too many zombies can prevent new process creation

**Process States Reference:**

| State | Meaning               |
| ----- | --------------------- |
| R     | Running or runnable   |
| S     | Interruptible sleep   |
| D     | Uninterruptible sleep |
| T     | Stopped               |
| **Z** | **Zombie (defunct)**  |

## Solution Steps

### Step 1 – Identify zombie processes

``` bash
# List all processes with their state
ps -eo pid,ppid,state,comm | grep 'Z'

# Or more precisely using awk
ps -eo pid,ppid,state,comm | awk '$3=="Z"'
```

**Output example:**
```
12345  12340  Z  defunct_process
12346  12340  Z  another_defunct
```

### Step 2 – Extract unique parent PIDs

``` bash
ps -eo pid,ppid,state,comm | awk '$3=="Z" {print $2}' | sort -u
```

**Explanation:**
- `$3=="Z"` → filter only zombie state
- `{print $2}` → print second column (PPID - parent PID)
- `sort -u` → remove duplicates (important: avoid restarting same service multiple times)

### Step 3 – Map parent PID to service name

``` bash
# Using systemctl
systemctl status <ppid>

# Or check cgroup
cat /proc/<ppid>/cgroup

# Or find the command name
ps -p <ppid> -o comm=
```

### Step 4 – Restart the parent service

``` bash
systemctl restart <service_name>
```

## Complete Script

```bash
#!/bin/bash

LOG_FILE="/var/log/zombie_cleanup.log"

echo "=== Zombie cleanup started at $(date) ===" >> "$LOG_FILE"

# Find unique parent PIDs of zombie processes
ZOMBIE_PARENTS=$(ps -eo pid,ppid,state,comm | awk '$3=="Z" {print $2}' | sort -u)

if [ -z "$ZOMBIE_PARENTS" ]; then
    echo "No zombie processes found" >> "$LOG_FILE"
    exit 0
fi

for ppid in $ZOMBIE_PARENTS; do
    # Get service name from systemd
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

## Interview Tips

**Why interviewers ask this:**
- Tests understanding of process lifecycle
- Tests ability to combine multiple Linux commands
- Tests scripting skills and error handling

**Key points to mention:**
1. Zombies can't be killed directly (they're already dead)
2. Only the parent process can clean them up by calling `wait()`
3. Restarting parent service forces cleanup
4. Always deduplicate PIDs to avoid unnecessary restarts

</details>

------------------------------------------------------------------------

<details>
<summary><b>2. Mapping Parent PID to Service</b></summary>

## Question

How do you map parent PIDs to system services?

## Why This Is Important

In production, you need to identify which service owns a problematic process before taking action. Random process killing can cause service outages.

## Methods to Map PID to Service

### Method 1: Using systemctl status

``` bash
systemctl status <pid>
```

**Output example:**
```
● nginx.service - The NGINX HTTP and reverse proxy server
   Main PID: 12340 (nginx)
   CGroup: /system.slice/nginx.service
           ├─12340 nginx: master process /usr/sbin/nginx
           └─12345 nginx: worker process
```

### Method 2: Check cgroup hierarchy

``` bash
cat /proc/<pid>/cgroup
```

**Output example:**
```
12:pids:/system.slice/nginx.service
11:memory:/system.slice/nginx.service
...
```

The service name appears after `/system.slice/`.

### Method 3: Use process tree

```bash
# Show process tree from PID
pstree -sp <pid>

# Output: systemd(1)───nginx(12340)───nginx(12345)
```

### Method 4: Check systemd unit for PID

```bash
# Find which unit owns the PID
systemctl status $(cat /proc/<pid>/cgroup | grep -oP 'system.slice/\K[^/]+' | head -1)
```

## Quick Reference Script

```bash
#!/bin/bash
# pid_to_service.sh - Map any PID to its systemd service

PID=$1

if [ -z "$PID" ]; then
    echo "Usage: $0 <pid>"
    exit 1
fi

# Method 1: Direct systemctl
echo "=== systemctl status ==="
systemctl status $PID 2>/dev/null | head -5

# Method 2: cgroup
echo -e "\n=== cgroup ==="
cat /proc/$PID/cgroup 2>/dev/null | grep service

# Method 3: Command name
echo -e "\n=== Process command ==="
ps -p $PID -o pid,ppid,comm,args
```

</details>

------------------------------------------------------------------------

<details>
<summary><b>3. Avoid Restarting Same Service Multiple Times</b></summary>

## Question

How do you prevent restarting the same service repeatedly if multiple
zombies share the same parent?

## The Problem

If a service spawns 10 zombie processes, a naive script would restart it 10 times!

```
Zombie1 → Parent 12340 → nginx.service (restart #1)
Zombie2 → Parent 12340 → nginx.service (restart #2) ← unnecessary!
Zombie3 → Parent 12340 → nginx.service (restart #3) ← unnecessary!
```

## Solution: Deduplicate Parent PIDs

``` bash
# Get unique parent PIDs only
ps -eo pid,ppid,state | awk '$3=="Z" {print $2}' | sort -u
```

**Breakdown:**

| Command                    | Purpose                    |
| -------------------------- | -------------------------- |
| `awk '$3=="Z" {print $2}'` | Extract PPID of zombies    |
| `sort -u`                  | Sort and remove duplicates |

## Alternative: Use associative array

```bash
#!/bin/bash
declare -A RESTARTED_SERVICES

ZOMBIE_PARENTS=$(ps -eo ppid,state | awk '$2=="Z" {print $1}')

for ppid in $ZOMBIE_PARENTS; do
    SERVICE=$(systemctl status $ppid 2>/dev/null | grep -oP '\S+\.service' | head -1)
    
    # Skip if already restarted
    if [ -n "${RESTARTED_SERVICES[$SERVICE]}" ]; then
        echo "Skipping $SERVICE (already restarted)"
        continue
    fi
    
    systemctl restart "$SERVICE"
    RESTARTED_SERVICES[$SERVICE]=1
    echo "Restarted: $SERVICE"
done
```

## Why This Matters in Interviews

Shows you understand:
- **Idempotency** - operations should be safe to repeat
- **Efficiency** - avoid unnecessary work
- **Production thinking** - minimize service disruption

</details>

------------------------------------------------------------------------

<details>
<summary><b>4. Docker Networking -- Packet Sniffing Problem</b></summary>

## Question

Why can containers sniff traffic on the same bridge network?

## Docker Bridge Network Architecture

When you run containers with default networking, Docker creates this structure:

```
┌─────────────────────────────────────────────────────┐
│                    HOST                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │Container1│  │Container2│  │Container3│          │
│  │  eth0    │  │  eth0    │  │  eth0    │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       │             │             │                 │
│       │  veth pair  │  veth pair  │  veth pair     │
│       │             │             │                 │
│  ┌────┴─────────────┴─────────────┴────┐           │
│  │           docker0 bridge             │           │
│  │      (Layer 2 broadcast domain)      │           │
│  └──────────────────┬──────────────────┘           │
│                     │                               │
│              ┌──────┴──────┐                        │
│              │  eth0 (host)│                        │
│              └─────────────┘                        │
└─────────────────────────────────────────────────────┘
```

## Why Sniffing Is Possible

The `docker0` bridge behaves like a **Layer 2 switch/hub**:

1. **Shared broadcast domain** - All containers on same bridge share L2 segment
2. **ARP is visible** - Containers can see ARP requests from neighbors
3. **Promiscuous mode** - Container with `NET_RAW` capability can enable promiscuous mode
4. **tcpdump works** - Tools like tcpdump can capture all traffic on the bridge

**Security implication:** A compromised container can potentially sniff traffic of other containers on the same bridge!

## Demonstration

```bash
# In Container1 (attacker)
tcpdump -i eth0 -n

# In Container2 (victim) - making HTTP request
curl http://some-api.com

# Container1 can see Container2's traffic!
```

## Components Explained

| Component              | Function                                        |
| ---------------------- | ----------------------------------------------- |
| **veth pair**          | Virtual ethernet - connects container to bridge |
| **docker0**            | Default Linux bridge for containers             |
| **Network namespace**  | Isolated network stack per container            |
| **NET_RAW capability** | Allows raw socket operations (sniffing)         |

</details>

------------------------------------------------------------------------

<details>
<summary><b>5. Isolating Container Traffic</b></summary>

## Question

How do you prevent containers from sniffing each other's traffic?

## Isolation Methods (Ranked by Effectiveness)

### Method 1: Separate Docker Networks (Recommended)

```bash
# Create isolated networks
docker network create app-network
docker network create db-network

# Run containers on separate networks
docker run --network app-network app-container
docker run --network db-network db-container
```

**Why it works:** Each network has its own bridge - no shared L2 domain.

```
┌─────────────┐     ┌─────────────┐
│ app-bridge  │     │ db-bridge   │
│ ┌─────────┐ │     │ ┌─────────┐ │
│ │Container│ │     │ │Container│ │
│ └─────────┘ │     │ └─────────┘ │
└─────────────┘     └─────────────┘
   ISOLATED            ISOLATED
```

### Method 2: Drop Network Capabilities

```bash
docker run --cap-drop=NET_RAW --cap-drop=NET_ADMIN myimage
```

| Capability  | What it allows                  |
| ----------- | ------------------------------- |
| `NET_RAW`   | Raw sockets, packet sniffing    |
| `NET_ADMIN` | Network configuration, iptables |

**Effect:** Container cannot run tcpdump or similar tools.

### Method 3: Macvlan Networking

```bash
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net
```

Each container gets its own MAC address and appears as a physical device.

### Method 4: Kubernetes Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Method 5: Encrypted Overlay Networks (Docker Swarm)

```bash
docker network create --opt encrypted --driver overlay secure-net
```

Traffic between nodes is encrypted with IPsec.

## Best Practice Recommendation

For production:
1. **Always use custom networks** (never default bridge)
2. **Drop NET_RAW capability** by default
3. **Use network policies** in Kubernetes
4. **Encrypt overlay traffic** for multi-host

</details>

------------------------------------------------------------------------

<details>
<summary><b>6. Macvlan Networking Deep Dive</b></summary>

## Question

How does macvlan prevent sniffing?

## How Macvlan Works

Macvlan assigns each container:
- **Unique MAC address**
- **Unique IP address**  
- **Direct connection to physical network**

```
┌────────────────────────────────────────────────┐
│              PHYSICAL NETWORK                   │
├────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │Container1│  │Container2│  │   Host   │     │
│  │MAC: aa:bb│  │MAC: cc:dd│  │MAC: ee:ff│     │
│  │IP: .101  │  │IP: .102  │  │IP: .1    │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│       │             │             │            │
│       └─────────────┴─────────────┘            │
│              Physical Switch                    │
└────────────────────────────────────────────────┘
```

**Why sniffing is prevented:**
- No shared bridge
- Each container is a separate L2 entity
- Physical switch handles traffic forwarding
- Container traffic doesn't pass through host bridge

## Creating Macvlan Network

```bash
# Create macvlan network
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  my-macvlan

# Run container
docker run --network my-macvlan --ip 192.168.1.100 nginx
```

## Important Limitation

**Containers CANNOT communicate with the host by default!**

```
Container (192.168.1.100) ←✗→ Host (192.168.1.1)
```

**Workaround:** Create a macvlan sub-interface on the host:

```bash
# Create macvlan interface on host
ip link add macvlan0 link eth0 type macvlan mode bridge
ip addr add 192.168.1.200/24 dev macvlan0
ip link set macvlan0 up

# Now host can communicate via 192.168.1.200
```

## Macvlan Modes

| Mode         | Behavior                                   |
| ------------ | ------------------------------------------ |
| **bridge**   | Containers can communicate with each other |
| **vepa**     | Traffic goes to external switch and back   |
| **private**  | Containers are completely isolated         |
| **passthru** | Single container gets direct NIC access    |

## When to Use Macvlan

✅ **Good for:**
- Legacy applications requiring specific IPs
- Applications that need to appear as physical hosts
- High-performance networking (no bridge overhead)

❌ **Avoid when:**
- Containers need to talk to host frequently
- Running in cloud (most clouds limit MAC addresses)
- You need simple container-to-container communication

</details>

------------------------------------------------------------------------

<details>
<summary><b>7. Kubernetes DNS Troubleshooting</b></summary>

## Question

Pods cannot resolve service names inside cluster. How do you troubleshoot?

## Understanding Kubernetes DNS

Every Kubernetes cluster runs CoreDNS (or kube-dns in older versions). When a pod does `curl my-service`, this happens:

```
┌─────────────────────────────────────────────────────────┐
│                    DNS Resolution Flow                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Pod: curl my-service                                    │
│         │                                                │
│         ▼                                                │
│  /etc/resolv.conf                                        │
│  nameserver 10.96.0.10 ←── kube-dns service IP          │
│         │                                                │
│         ▼                                                │
│  CoreDNS Pod (kube-system)                              │
│         │                                                │
│         ▼                                                │
│  Kubernetes API Server                                   │
│         │                                                │
│         ▼                                                │
│  Service → Endpoints → Pod IPs                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Systematic Debugging Steps

### Step 1 – Test DNS from inside a pod

```bash
# Launch debug pod and test
kubectl run dnstest --image=busybox:1.28 --rm -it --restart=Never -- nslookup kubernetes.default

# Expected output:
# Server:    10.96.0.10
# Address:   10.96.0.10:53
# Name:      kubernetes.default.svc.cluster.local
# Address:   10.96.0.1
```

If this fails → DNS is broken.

### Step 2 – Check pod's DNS configuration

```bash
kubectl exec <pod-name> -- cat /etc/resolv.conf
```

**Expected output:**
```
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

| Field        | Purpose                                       |
| ------------ | --------------------------------------------- |
| `nameserver` | CoreDNS service IP                            |
| `search`     | Domain suffixes to try                        |
| `ndots:5`    | If name has <5 dots, try search domains first |

### Step 3 – Verify CoreDNS pods are running

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

**Check for:**
- Pods in `Running` state
- No restarts (CrashLoopBackOff indicates issues)
- Multiple replicas for HA

### Step 4 – Check CoreDNS logs

```bash
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50
```

**Common errors:**
- `SERVFAIL` → upstream DNS issue
- `NXDOMAIN` → service doesn't exist
- `connection refused` → network policy blocking

### Step 5 – Inspect CoreDNS ConfigMap

```bash
kubectl get configmap coredns -n kube-system -o yaml
```

**Key plugins to verify:**
```
.:53 {
    errors              # Log errors
    health              # Health check endpoint
    kubernetes cluster.local {  # Handle cluster DNS
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
    }
    forward . /etc/resolv.conf  # Forward external DNS
    cache 30            # Cache responses
    loop                # Detect forwarding loops
    reload              # Auto-reload config
}
```

### Step 6 – Verify kube-dns service and endpoints

```bash
# Check service
kubectl get svc kube-dns -n kube-system

# Check endpoints (should show CoreDNS pod IPs)
kubectl get endpoints kube-dns -n kube-system
```

**If endpoints are empty:** CoreDNS pods are not ready or selector doesn't match.

### Step 7 – Check Network Policies

```bash
kubectl get networkpolicy -A
```

**DNS requires:**
- **UDP port 53** - standard DNS queries
- **TCP port 53** - large responses, zone transfers

If network policies exist, ensure DNS traffic is allowed:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
spec:
  podSelector: {}
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

## Quick DNS Debugging Checklist

| Check            | Command                                               |
| ---------------- | ----------------------------------------------------- |
| DNS resolution   | `nslookup kubernetes.default`                         |
| Pod DNS config   | `cat /etc/resolv.conf`                                |
| CoreDNS pods     | `kubectl get pods -n kube-system -l k8s-app=kube-dns` |
| CoreDNS logs     | `kubectl logs -n kube-system -l k8s-app=kube-dns`     |
| DNS service      | `kubectl get svc,ep kube-dns -n kube-system`          |
| Network policies | `kubectl get netpol -A`                               |

</details>

------------------------------------------------------------------------

<details>
<summary><b>8. CrashLoopBackOff Debugging</b></summary>

## Question

A pod is in CrashLoopBackOff. How do you debug it?

## Understanding CrashLoopBackOff

**CrashLoopBackOff** means:
1. Container starts
2. Container crashes/exits
3. Kubernetes restarts it
4. It crashes again
5. Kubernetes applies exponential backoff (10s, 20s, 40s... up to 5min)

```
┌────────────────────────────────────────────┐
│           CrashLoopBackOff Timeline         │
├────────────────────────────────────────────┤
│                                             │
│  Start → Crash → Wait 10s →                │
│  Start → Crash → Wait 20s →                │
│  Start → Crash → Wait 40s →                │
│  Start → Crash → Wait 80s →                │
│  Start → Crash → Wait 160s →               │
│  Start → Crash → Wait 300s (max) →         │
│                                             │
└────────────────────────────────────────────┘
```

## Systematic Debugging Steps

### Step 1 – Get pod events and status

```bash
kubectl describe pod <pod-name>
```

**Look for:**
- `Last State` → Exit code and reason
- `Events` → Why it failed

**Common exit codes:**

| Exit Code | Meaning                                 |
| --------- | --------------------------------------- |
| 0         | Success (but container shouldn't exit!) |
| 1         | Application error                       |
| 137       | SIGKILL (OOMKilled or manual kill)      |
| 139       | SIGSEGV (segmentation fault)            |
| 143       | SIGTERM (graceful shutdown)             |

### Step 2 – Check current and previous logs

```bash
# Current container logs
kubectl logs <pod-name>

# Previous container logs (crucial for crashes!)
kubectl logs <pod-name> --previous

# With timestamps
kubectl logs <pod-name> --previous --timestamps
```

### Step 3 – Check resource constraints

```bash
# Pod resource usage
kubectl top pod <pod-name>

# Node resources
kubectl describe node <node-name> | grep -A5 "Allocated resources"
```

**OOMKilled?** Container exceeded memory limit:
```yaml
resources:
  limits:
    memory: "128Mi"  # Increase if needed
```

### Step 4 – Verify probes configuration

```bash
kubectl get pod <pod-name> -o yaml | grep -A10 "livenessProbe\|readinessProbe"
```

**Common probe issues:**
- Probe path incorrect
- Probe port wrong
- initialDelaySeconds too short
- Application takes longer to start than timeout

**Fix example:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30  # Give app time to start
  periodSeconds: 10
  failureThreshold: 3
```

### Step 5 – Check configuration and secrets

```bash
# Check if ConfigMaps exist
kubectl get configmap

# Check if Secrets exist
kubectl get secrets

# Verify environment variables
kubectl get pod <pod-name> -o yaml | grep -A20 "env:"
```

### Step 6 – Debug with interactive shell

```bash
# Override entrypoint to keep container running
kubectl run debug --image=<same-image> --rm -it --command -- /bin/sh

# Or modify deployment temporarily
# Change command to: ["sleep", "infinity"]
```

## CrashLoopBackOff Causes Checklist

| Cause                      | How to Identify                             |
| -------------------------- | ------------------------------------------- |
| **Application bug**        | Check logs for stack traces                 |
| **Missing config**         | Check for ConfigMap/Secret errors in events |
| **OOMKilled**              | Exit code 137, check `kubectl describe pod` |
| **Liveness probe failing** | Events show "Liveness probe failed"         |
| **Missing dependencies**   | Logs show connection refused/timeout        |
| **Permission issues**      | Logs show "permission denied"               |
| **Image issues**           | Events show ImagePullBackOff first          |

</details>

------------------------------------------------------------------------

<details>
<summary><b>9. OOMKilled Pod</b></summary>

## Question

Pod was OOMKilled. What happened and how do you fix it?

## Understanding OOMKilled

**OOMKilled** = **O**ut **O**f **M**emory **Killed**

The Linux kernel's OOM (Out of Memory) Killer terminated the container because it exceeded its memory limit.

```
┌────────────────────────────────────────────┐
│           OOMKilled Flow                    │
├────────────────────────────────────────────┤
│                                             │
│  Container requests 256Mi                   │
│         │                                   │
│         ▼                                   │
│  Application uses 260Mi                     │
│         │                                   │
│         ▼                                   │
│  Kernel OOM Killer activates               │
│         │                                   │
│         ▼                                   │
│  Container killed (exit code 137)          │
│         │                                   │
│         ▼                                   │
│  Kubernetes restarts container             │
│                                             │
└────────────────────────────────────────────┘
```

## How to Identify OOMKilled

### Method 1: kubectl describe

```bash
kubectl describe pod <pod-name>
```

**Look for:**
```
Last State:     Terminated
  Reason:       OOMKilled
  Exit Code:    137
```

### Method 2: Check events

```bash
kubectl get events --field-selector involvedObject.name=<pod-name>
```

### Method 3: Node-level check

```bash
dmesg | grep -i "killed process"
```

## Why OOMKilled Happens

| Cause                         | Description                                |
| ----------------------------- | ------------------------------------------ |
| **Memory limit too low**      | Limit doesn't match application needs      |
| **Memory leak**               | Application gradually consumes more memory |
| **Traffic spike**             | More requests = more memory                |
| **JVM heap misconfiguration** | Java heap larger than container limit      |
| **No limits set**             | Container grows until node runs out        |

## How to Fix

### Option 1: Increase memory limit

```yaml
resources:
  requests:
    memory: "256Mi"
  limits:
    memory: "512Mi"  # Increase limit
```

### Option 2: Optimize application

```bash
# Profile memory usage
kubectl top pod <pod-name>

# Check actual memory consumption over time
kubectl exec <pod-name> -- cat /sys/fs/cgroup/memory/memory.usage_in_bytes
```

### Option 3: For Java applications

**Common mistake:** JVM heap larger than container limit

```yaml
env:
- name: JAVA_OPTS
  value: "-Xms256m -Xmx384m"  # Keep below container limit!

resources:
  limits:
    memory: "512Mi"  # Must be > Xmx + overhead (~30%)
```

**Rule of thumb for Java:**
```
Container limit = Xmx + 150Mi (for metaspace, stack, native memory)
```

### Option 4: Enable memory monitoring

```bash
# Real-time memory monitoring
watch kubectl top pod <pod-name>
```

## Best Practices

1. **Always set memory limits** - Prevent runaway containers
2. **Set requests = limits for critical pods** - Guaranteed QoS class
3. **Monitor memory trends** - Use Prometheus + Grafana
4. **Configure JVM properly** - Use `-XX:MaxRAMPercentage=75`
5. **Test under load** - Profile before production

## Quick Reference

```yaml
# Recommended configuration
resources:
  requests:
    memory: "256Mi"    # Scheduler uses this
    cpu: "250m"
  limits:
    memory: "512Mi"    # Hard limit (OOMKill if exceeded)
    cpu: "500m"        # Throttled, not killed
```

</details>

------------------------------------------------------------------------

<details>
<summary><b>10. Prometheus Alerting Strategy</b></summary>

## Question

How do you design an alerting strategy that reduces alert fatigue?

## The Alert Fatigue Problem

**Alert fatigue** occurs when engineers receive too many alerts, leading to:
- Ignored alerts
- Delayed response to real issues
- Burnout
- Missed critical incidents

**Goal:** Only alert on **actionable, impactful issues**.

## Best Practices for Alerting

### 1. Use Severity Levels

```yaml
# Critical - Wake someone up at 3 AM
- alert: ServiceDown
  expr: up{job="api"} == 0
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "API service is down"

# Warning - Fix during business hours
- alert: HighMemoryUsage
  expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.85
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "Memory usage above 85%"

# Info - Log for review, no notification
- alert: SlowQueries
  expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
  labels:
    severity: info
```

### 2. Use `for` Duration (Avoid Flapping)

```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
for: 10m  # Must be true for 10 minutes before firing
```

**Why?** Prevents alerts from brief spikes that auto-resolve.

### 3. Alert on SLOs, Not Symptoms

**Bad:** Alert on every 500 error
**Good:** Alert when error budget is being consumed

```yaml
# SLO-based alerting (error budget burn rate)
- alert: HighErrorBudgetBurn
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (1 - 0.999) * 14.4  # Burning 14.4x faster than allowed
  for: 5m
  labels:
    severity: critical
```

### 4. Alert on User Impact

```yaml
# Alert when users are affected
- alert: UserFacingErrors
  expr: |
    sum(rate(http_requests_total{status=~"5..", endpoint="/api/checkout"}[5m])) 
    / 
    sum(rate(http_requests_total{endpoint="/api/checkout"}[5m])) > 0.01
  for: 5m
  annotations:
    summary: "Checkout endpoint error rate > 1%"
```

### Alerting Pyramid

```
              ┌───────────────┐
              │   Critical    │  ← Page (PagerDuty)
              │  (Immediate)  │
              └───────┬───────┘
                      │
            ┌─────────┴─────────┐
            │     Warning       │  ← Slack notification
            │ (Business hours)  │
            └─────────┬─────────┘
                      │
        ┌─────────────┴─────────────┐
        │          Info             │  ← Dashboard only
        │   (Review in standup)     │
        └───────────────────────────┘
```

## Complete Example Alert Rule

```yaml
groups:
- name: api-alerts
  rules:
  - alert: HighErrorRate
    expr: |
      sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
      /
      sum(rate(http_requests_total[5m])) by (service)
      > 0.05
    for: 10m
    labels:
      severity: critical
      team: platform
    annotations:
      summary: "High error rate on {{ $labels.service }}"
      description: "Error rate is {{ printf \"%.2f\" $value | humanizePercentage }}"
      runbook_url: "https://wiki.company.com/runbooks/high-error-rate"
```

## Alerting Checklist

| Question                   | Answer                            |
| -------------------------- | --------------------------------- |
| Is it actionable?          | Someone can do something about it |
| Is it impactful?           | Users or business are affected    |
| Is it urgent?              | Needs immediate attention         |
| Has proper `for` duration? | Avoids flapping                   |
| Has runbook link?          | Engineer knows what to do         |

</details>

------------------------------------------------------------------------

<details>
<summary><b>11. Alertmanager Grouping</b></summary>

## Question

How does Alertmanager grouping work and why is it important?

## The Problem Without Grouping

Without grouping, if 50 pods fail health checks:
- You get **50 separate notifications**
- Your Slack channel is flooded
- Engineers ignore alerts

## How Grouping Works

Alertmanager **batches related alerts** into single notifications.

```
┌─────────────────────────────────────────────────┐
│              Without Grouping                    │
├─────────────────────────────────────────────────┤
│  Alert: Pod nginx-1 down                        │
│  Alert: Pod nginx-2 down                        │
│  Alert: Pod nginx-3 down     → 50 notifications │
│  ... 47 more alerts ...                         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│              With Grouping                       │
├─────────────────────────────────────────────────┤
│  Alert Group: PodDown                           │
│  Service: nginx                                 │
│  Affected pods: 50          → 1 notification    │
└─────────────────────────────────────────────────┘
```

## Configuration

```yaml
route:
  # How to group alerts
  group_by: ['alertname', 'service', 'cluster']
  
  # Wait time before sending first notification
  group_wait: 30s
  
  # Wait time before sending updates to existing group
  group_interval: 5m
  
  # Wait time before resending resolved notification
  repeat_interval: 4h
  
  receiver: default-receiver
  
  # Child routes for specific alerts
  routes:
  - match:
      severity: critical
    receiver: pagerduty
    group_wait: 10s  # Faster for critical
    
  - match:
      severity: warning
    receiver: slack
    group_wait: 1m
```

## Timing Parameters Explained

| Parameter         | Purpose                             | Typical Value |
| ----------------- | ----------------------------------- | ------------- |
| `group_wait`      | Wait for more alerts before sending | 30s - 1m      |
| `group_interval`  | Min time between updates            | 5m            |
| `repeat_interval` | Resend if still firing              | 4h            |

## Grouping Example

```yaml
# Group by service - all pods from same service in one alert
group_by: ['alertname', 'service']

# Scenario:
# - nginx-pod-1 fires HighMemory
# - nginx-pod-2 fires HighMemory
# - nginx-pod-3 fires HighMemory
# 
# Result: ONE notification for "HighMemory on service=nginx"
```

## Best Practices

1. **Group by service** - Related issues together
2. **Short group_wait for critical** - Don't delay urgent alerts
3. **Longer group_wait for warning** - Batch non-urgent alerts
4. **Don't over-group** - Separate unrelated issues

</details>

------------------------------------------------------------------------

<details>
<summary><b>12. Alert Inhibition</b></summary>

## Question

What is alert inhibition and when would you use it?

## The Problem

When a critical issue occurs, it often causes secondary alerts:

```
Primary alert:    Node down
Secondary alerts: Pod unreachable (x20)
                  Disk unavailable (x5)
                  Service unhealthy (x10)
                  
Total: 36 alerts for ONE root cause!
```

## How Inhibition Works

Inhibition **suppresses secondary alerts** when a primary alert is firing.

```yaml
inhibit_rules:
  # When node is down, suppress pod alerts on that node
  - source_match:
      alertname: NodeDown
    target_match:
      alertname: PodUnreachable
    equal: ['node']  # Only inhibit if same node
    
  # Critical alerts suppress related warnings
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['service']  # Only inhibit same service
```

## Configuration Explained

```yaml
inhibit_rules:
  - source_match:      # The "primary" alert
      severity: critical
    target_match:      # The "secondary" alert to suppress
      severity: warning
    equal: ['service', 'cluster']  # Match these labels
```

| Field          | Purpose                                          |
| -------------- | ------------------------------------------------ |
| `source_match` | Labels that identify the primary alert           |
| `target_match` | Labels that identify alerts to suppress          |
| `equal`        | Labels that must match between source and target |

## Real-World Examples

### Example 1: Infrastructure hierarchy

```yaml
# Database down → suppress app alerts
- source_match:
    alertname: DatabaseDown
  target_match:
    alertname: AppSlowResponse
  equal: ['database']

# Network down → suppress all service alerts
- source_match:
    alertname: NetworkPartition
  target_match_re:
    alertname: '.+'
  equal: ['datacenter']
```

### Example 2: Severity-based

```yaml
# Critical suppresses warning for same service
- source_match:
    severity: critical
  target_match:
    severity: warning
  equal: ['service', 'namespace']
```

## Inhibition Flow

```
┌─────────────────────────────────────────────┐
│           Alert Processing Flow              │
├─────────────────────────────────────────────┤
│                                              │
│  New Alert Arrives                           │
│       │                                      │
│       ▼                                      │
│  Check Inhibition Rules                      │
│       │                                      │
│   ┌───┴───┐                                  │
│   │Match? │                                  │
│   └───┬───┘                                  │
│       │                                      │
│   YES │        NO                            │
│       │         │                            │
│       ▼         ▼                            │
│  Suppressed   Process → Group → Notify      │
│                                              │
└─────────────────────────────────────────────┘
```

## Best Practices

1. **Don't over-inhibit** - Important alerts might be hidden
2. **Use `equal` carefully** - Be specific about what matches
3. **Test inhibition rules** - Verify they work as expected
4. **Document rules** - Team should understand what's suppressed

</details>

------------------------------------------------------------------------

<details>
<summary><b>13. Secure Multi-Account CI/CD Pipeline</b></summary>

## Question

How do you design a secure CI/CD pipeline across multiple AWS accounts?

## Why Multi-Account?

Organizations use separate AWS accounts for:
- **Development** - Experimentation, less restrictions
- **Staging** - Pre-production testing
- **Production** - Customer-facing, highest security

**Security principle:** Isolation prevents blast radius expansion.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    Secure CI/CD Pipeline                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  DEVELOPMENT ACCOUNT              SHARED SERVICES ACCOUNT         │
│  ┌──────────────────┐            ┌──────────────────┐            │
│  │   Developer      │            │    Artifact      │            │
│  │   commits code   │───────────▶│    Repository    │            │
│  └──────────────────┘            │   (ECR / S3)     │            │
│                                   └────────┬─────────┘            │
│                                            │                      │
│  CI ACCOUNT                                │                      │
│  ┌──────────────────┐                     │                      │
│  │   Build          │◀────────────────────┘                      │
│  │   Test           │                                            │
│  │   Scan           │                                            │
│  │   Sign           │────────────┐                               │
│  └──────────────────┘            │                               │
│                                   │                               │
│  PRODUCTION ACCOUNT              │                               │
│  ┌──────────────────┐            │                               │
│  │   Deployment     │◀───────────┘                               │
│  │   Role           │    (cross-account assume role)            │
│  └──────────────────┘                                            │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Security Controls

### 1. IAM Least Privilege

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage"
      ],
      "Resource": "arn:aws:ecr:us-east-1:111111111111:repository/app"
    }
  ]
}
```

### 2. Cross-Account Roles

**In Production Account:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::222222222222:role/ci-pipeline-role"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "secure-external-id"
        }
      }
    }
  ]
}
```

**CI Pipeline assumes this role:**
```bash
aws sts assume-role \
  --role-arn arn:aws:iam::333333333333:role/production-deploy-role \
  --role-session-name "ci-deployment" \
  --external-id "secure-external-id"
```

### 3. Artifact Signing

Ensure artifacts are trusted before deployment:

```
┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐    ┌────────┐
│ Build │───▶│ Scan  │───▶│ Sign  │───▶│Verify │───▶│ Deploy │
└───────┘    └───────┘    └───────┘    └───────┘    └────────┘
```

### 4. Service Control Policies (SCPs)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDirectProdAccess",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/ci-deployment-role"
        }
      }
    }
  ]
}
```

## Pipeline Stages

| Stage             | Account    | Actions                               |
| ----------------- | ---------- | ------------------------------------- |
| 1. Build          | CI         | Compile, unit tests                   |
| 2. Scan           | CI         | SAST, container scanning              |
| 3. Sign           | CI         | Sign artifact with AWS Signer         |
| 4. Store          | Shared     | Push to ECR/S3                        |
| 5. Deploy Staging | Staging    | Assume role, deploy, test             |
| 6. Deploy Prod    | Production | Assume role, verify signature, deploy |

## Interview Answer Framework

> "I would design a multi-account pipeline with:
> 1. **Separate accounts** for CI, staging, production
> 2. **Cross-account IAM roles** with least privilege
> 3. **Artifact signing** using cosign or AWS Signer
> 4. **SCPs** to prevent direct production access
> 5. **CloudTrail** for audit logging across all accounts"

</details>

------------------------------------------------------------------------

<details>
<summary><b>14. Artifact Signing</b></summary>

## Question

How do you ensure container images are trusted before deployment?

## Why Artifact Signing?

Without signing, anyone with registry access could:
- Push malicious images
- Overwrite legitimate tags
- Deploy compromised code

**Artifact signing provides:**
- **Integrity** - Image hasn't been modified
- **Authenticity** - Image came from trusted source
- **Non-repudiation** - Clear audit trail

## Supply Chain Flow

```
┌─────────────────────────────────────────────────────────────┐
│              Secure Supply Chain                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐ │
│  │Source │──▶│ Build │──▶│ Scan  │──▶│ Sign  │──▶│ Store │ │
│  │ Code  │   │       │   │       │   │       │   │       │ │
│  └───────┘   └───────┘   └───────┘   └───────┘   └───────┘ │
│                                                      │       │
│                                                      ▼       │
│                                              ┌───────────┐   │
│                                              │  Verify   │   │
│                                              │ Signature │   │
│                                              └─────┬─────┘   │
│                                                    │         │
│                                                    ▼         │
│                                              ┌───────────┐   │
│                                              │  Deploy   │   │
│                                              └───────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Tools for Artifact Signing

### 1. Cosign (Sigstore) - Most Popular

```bash
# Sign image
cosign sign --key cosign.key myregistry.com/myapp:v1.0.0

# Verify before deployment
cosign verify --key cosign.pub myregistry.com/myapp:v1.0.0
```

### 2. AWS Signer

```bash
# Create signing profile
aws signer put-signing-profile \
  --profile-name ProductionSigning \
  --platform-id AmazonContainer

# Sign container image
aws signer start-signing-job \
  --source 's3://bucket/unsigned-image.tar' \
  --destination 's3://bucket/signed/' \
  --profile-name ProductionSigning
```

### 3. Notary / Docker Content Trust

```bash
# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Push automatically signs
docker push myregistry.com/myapp:v1.0.0
```

## Kubernetes Integration

### Using Kyverno (Policy Engine)

```yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: verify-image-signature
spec:
  validationFailureAction: enforce
  rules:
  - name: verify-signature
    match:
      resources:
        kinds:
        - Pod
    verifyImages:
    - image: "myregistry.com/*"
      key: |-
        -----BEGIN PUBLIC KEY-----
        MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
        -----END PUBLIC KEY-----
```

### Using OPA Gatekeeper

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: require-signed-images
spec:
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
  parameters:
    repos:
    - "trusted-registry.com/"
```

## Best Practices

| Practice                     | Why                       |
| ---------------------------- | ------------------------- |
| Sign in CI pipeline          | Automate, no manual steps |
| Use keyless signing (Fulcio) | No key management         |
| Store signatures in registry | Co-located with images    |
| Verify at deployment time    | Last line of defense      |
| Rotate keys regularly        | Limit blast radius        |

</details>

------------------------------------------------------------------------

<details>
<summary><b>15. Prevent Developers from Bypassing Pipeline</b></summary>

## Question

How do you prevent developers from deploying directly to production, bypassing the CI/CD pipeline?

## Defense in Depth Approach

No single control is sufficient. Use **multiple layers**:

```
┌─────────────────────────────────────────────────────────┐
│              Defense in Depth                            │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: IAM Policies                                  │
│     ├── No direct production access for developers      │
│     └── Only CI role can deploy                         │
│                                                          │
│  Layer 2: Service Control Policies (SCPs)               │
│     └── Organization-level deny rules                   │
│                                                          │
│  Layer 3: Kubernetes RBAC                               │
│     └── No direct kubectl access to prod                │
│                                                          │
│  Layer 4: GitOps                                        │
│     └── All changes through Git + ArgoCD               │
│                                                          │
│  Layer 5: Audit & Alerting                              │
│     └── Alert on any direct access attempts            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Implementation Methods

### Method 1: Remove Direct IAM Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyProductionAccess",
      "Effect": "Deny",
      "Action": [
        "eks:*",
        "ecs:*",
        "ec2:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Environment": "production"
        }
      }
    }
  ]
}
```

### Method 2: Service Control Policies (Account-Level)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforcePipelineDeployment",
      "Effect": "Deny",
      "Action": [
        "ecs:UpdateService",
        "eks:UpdateNodegroupConfig",
        "lambda:UpdateFunctionCode"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/ci-deployment-*"
        }
      }
    }
  ]
}
```

### Method 3: Kubernetes RBAC

```yaml
# Read-only access for developers
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: developer-readonly
rules:
- apiGroups: [""]
  resources: ["pods", "services", "deployments"]
  verbs: ["get", "list", "watch"]  # No create/update/delete!

---
# Full access only for CI service account
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ci-deployer
rules:
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

### Method 4: GitOps Enforcement

```yaml
# ArgoCD Application - only syncs from Git
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
spec:
  source:
    repoURL: https://github.com/company/k8s-manifests
    targetRevision: main
    path: production
  destination:
    server: https://production-cluster
    namespace: app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true  # Reverts any manual changes!
```

### Method 5: Enforce IaC for All Changes

```hcl
# Terraform state locking
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # Prevents concurrent changes
  }
}
```

## Summary Table

| Control      | What It Prevents              |
| ------------ | ----------------------------- |
| IAM Deny     | Direct AWS console/CLI access |
| SCPs         | Organization-wide enforcement |
| K8s RBAC     | Direct kubectl apply          |
| GitOps       | Manual manifest changes       |
| IaC          | Infrastructure drift          |
| Audit alerts | Detection of bypass attempts  |

</details>

------------------------------------------------------------------------

<details>
<summary><b>16. Auditing Pipeline Activity</b></summary>

## Question

How do you audit and monitor CI/CD pipeline activity for security?

## Why Auditing Matters

You need to answer:
- **Who** deployed what?
- **When** was it deployed?
- **What** changed?
- **Did** anything suspicious happen?

## AWS Auditing Tools

### 1. CloudTrail - API Activity

```bash
# Enable CloudTrail for all regions
aws cloudtrail create-trail \
  --name organization-trail \
  --s3-bucket-name audit-logs \
  --is-multi-region-trail \
  --include-global-service-events
```

**Key events to track:**
- `AssumeRole` - Cross-account access
- `UpdateService` - ECS deployments
- `UpdateDeployment` - EKS changes
- `PutImage` - ECR pushes

### 2. CloudWatch Alarms

```yaml
# Alert on direct production access
Resources:
  DirectAccessAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: DirectProductionAccess
      MetricName: UnauthorizedAccessAttempts
      Namespace: Security
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - !Ref SecuritySNSTopic
```

### 3. AWS Config Rules

```yaml
# Ensure all deployments are from approved sources
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  ConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: approved-deployment-sources
      Source:
        Owner: CUSTOM_LAMBDA
        SourceIdentifier: !GetAtt AuditLambda.Arn
```

### 4. GuardDuty - Threat Detection

```bash
# Enable GuardDuty
aws guardduty create-detector --enable
```

**Detects:**
- Unusual API calls
- Compromised credentials
- Cryptocurrency mining
- Unauthorized access patterns

## Centralized Logging Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Centralized Audit Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ Dev Acc │  │Stage Acc│  │Prod Acc │                     │
│  └────┬────┘  └────┬────┘  └────┬────┘                     │
│       │            │            │                           │
│       └────────────┴────────────┘                           │
│                    │                                         │
│                    ▼                                         │
│         ┌──────────────────┐                                │
│         │  Log Archive     │  (Centralized S3 bucket)       │
│         │  Account         │                                │
│         └────────┬─────────┘                                │
│                  │                                           │
│        ┌─────────┴─────────┐                                │
│        ▼                   ▼                                │
│  ┌───────────┐      ┌───────────┐                          │
│  │CloudWatch │      │  Athena   │                          │
│  │ Insights  │      │ Queries   │                          │
│  └───────────┘      └───────────┘                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Example Athena Query

```sql
-- Find all assume role events in last 24 hours
SELECT 
    eventtime,
    useridentity.arn as assumed_by,
    requestparameters.rolearn as role_assumed,
    sourceipaddress
FROM cloudtrail_logs
WHERE eventname = 'AssumeRole'
  AND eventtime > date_add('hour', -24, now())
ORDER BY eventtime DESC;
```

## Audit Checklist

| Item            | Tool                | Purpose                |
| --------------- | ------------------- | ---------------------- |
| API calls       | CloudTrail          | Who did what           |
| Deployments     | CloudWatch Events   | When changes happened  |
| Config drift    | AWS Config          | Infrastructure changes |
| Threats         | GuardDuty           | Security anomalies     |
| Access patterns | CloudTrail Insights | Unusual behavior       |

</details>

------------------------------------------------------------------------

<details>
<summary><b>Key Interview Takeaway - Structured Debugging Framework</b></summary>

## The Golden Rule

Most DevOps troubleshooting questions follow this pattern:

```
┌───────────────────────────────────────────────────┐
│           Structured Debugging Flow               │
├───────────────────────────────────────────────────┤
│                                                    │
│  1. IDENTIFY                                      │
│     └── What is the symptom?                      │
│                                                    │
│  2. INSPECT LOGS                                  │
│     └── Application, container, system logs       │
│                                                    │
│  3. VERIFY CONFIG                                 │
│     └── Environment variables, secrets, configs   │
│                                                    │
│  4. CHECK INFRASTRUCTURE                          │
│     └── Network, resources, dependencies          │
│                                                    │
│  5. FIX & VERIFY                                  │
│     └── Apply fix, confirm resolution            │
│                                                    │
└───────────────────────────────────────────────────┘
```

## Layered Analysis Approach

Always debug from top to bottom:

```
Application    → Logs, errors, stack traces
     │
     ▼
Container      → Resource limits, restarts, state
     │
     ▼
Kubernetes     → Events, RBAC, network policies
     │
     ▼
Network        → DNS, connectivity, latency
     │
     ▼
Cloud          → IAM, VPC, load balancers
```

## Interview Answer Template

When answering troubleshooting questions, use this structure:

> **"First**, I would verify [immediate symptom check].
> 
> **Then**, I would inspect [relevant logs/metrics].
> 
> **Next**, I would check [configuration/infrastructure].
> 
> **If the issue persists**, I would investigate [deeper causes].
> 
> **Finally**, I would implement [fix] and verify [resolution]."

## Example: Slow API Response

> "First, I would check application logs for errors or slow queries.
> 
> Then, I would verify container CPU and memory usage using `kubectl top`.
> 
> Next, I would check for pod restarts or resource throttling.
> 
> If those look fine, I would investigate network latency between services.
> 
> Finally, I would check cloud load balancer metrics and target health."

## Why This Matters

Interviewers score highly on:

| Trait                     | How You Show It                   |
| ------------------------- | --------------------------------- |
| **Systematic thinking**   | Follow a clear debugging order    |
| **Depth of knowledge**    | Know the right tools and commands |
| **Production experience** | Mention monitoring, logs, metrics |
| **Communication**         | Explain your thought process      |

## Quick Reference Commands

```bash
# Kubernetes
kubectl describe pod <pod>
kubectl logs <pod> --previous
kubectl top pod <pod>
kubectl get events --sort-by='.lastTimestamp'

# Docker
docker logs <container>
docker stats <container>
docker inspect <container>

# Linux
dmesg | tail -50
journalctl -u <service> -f
top -bn1 | head -20
```

</details>

------------------------------------------------------------------------

# End of Guide
