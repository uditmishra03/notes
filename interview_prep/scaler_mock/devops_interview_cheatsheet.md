
# DevOps L1/L2 Interview Cheat Sheet (Mock Interview Revision)

This document consolidates the **questions, strong interview answers, key commands, and common follow‑ups** from the mock interview session.  
Use it as a quick **revision guide before interviews**.

---

# 1. Zombie Processes Debugging (Linux)

## Question
How would you detect zombie processes and restart the parent service?

## Key Concept
Zombie processes have finished execution but their parent process hasn't collected the exit status.

State:

```
Z → Zombie
```

## Detection

```bash
ps -eo pid,ppid,state,comm | awk '$3=="Z"'
```

Extract parent PIDs:

```bash
ps -eo pid,ppid,state | awk '$3=="Z"{print $2}' | sort -u
```

Restart parent service:

```bash
systemctl status <pid>
systemctl restart <service>
```

## Follow-up interview point
Deduplicate PIDs so the service restarts only once.

---

# 2. Mapping PID to System Service

## Question
How do you determine which systemd service owns a PID?

Commands:

```
systemctl status <pid>
```

or

```
cat /proc/<pid>/cgroup
```

Example output:

```
/system.slice/nginx.service
```

---

# 3. Docker Networking – Why Containers Can Sniff Traffic

Docker networking uses:

```
container → veth → linux bridge → veth → container
```

The **Linux bridge behaves like an L2 switch**.

Containers connected to the same bridge share the **same broadcast domain**.

Tools like:

```
tcpdump
wireshark
```

may capture packets if privileges allow.

---

# 4. How to Isolate Container Traffic

Methods:

1. Separate bridge networks
2. macvlan network
3. Kubernetes network policies
4. Drop NET_RAW capability

Example:

```
docker run --cap-drop NET_RAW
```

---

# 5. Macvlan Networking

## Concept

Macvlan assigns:

```
unique MAC
unique IP
direct network access
```

Containers appear as **independent hosts on the network**.

### Advantage
Better isolation.

### Drawback
Containers cannot communicate with the host by default.

---

# 6. Kubernetes DNS Troubleshooting

### Step 1 – Test DNS inside pod

```
kubectl run dns-test --image=busybox -it --rm -- sh
nslookup kubernetes.default
```

### Step 2 – Inspect pod DNS config

```
cat /etc/resolv.conf
```

Expected:

```
nameserver <coredns-ip>
search svc.cluster.local
```

### Step 3 – Verify CoreDNS

```
kubectl get pods -n kube-system
kubectl logs -n kube-system <coredns-pod>
```

### Step 4 – Check service

```
kubectl get svc -n kube-system
kubectl get endpoints kube-dns -n kube-system
```

---

# 7. CrashLoopBackOff Debugging

Common causes:

```
bad configuration
failed probes
application crash
resource limits
```

Debug flow:

```
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
```

Then check:

```
livenessProbe
readinessProbe
resources
environment variables
```

---

# 8. OOMKilled Containers

## Cause

Container exceeded memory limit.

Check:

```
kubectl describe pod <pod>
kubectl top pod <pod>
```

Example:

```
Reason: OOMKilled
Exit Code: 137
```

## Fix

Increase memory limits or optimize application.

Example:

```yaml
resources:
  requests:
    memory: "512Mi"
  limits:
    memory: "1Gi"
```

---

# 9. Prometheus Alerting Strategy

Goal: **avoid alert fatigue**

Best practices:

```
severity labels
time windows
grouping
inhibition
SLO alerts
```

Example rule:

```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
for: 10m
```

---

# 10. Alertmanager Grouping

Example:

```yaml
route:
  group_by: ["alertname","service"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
```

Purpose:

```
combine multiple alerts into one notification
```

---

# 11. Alertmanager Inhibition

Suppress secondary alerts when a major alert fires.

Example:

```yaml
inhibit_rules:
- source_match:
    severity: critical
  target_match:
    severity: warning
  equal: ["service"]
```

Example scenario:

```
ServiceDown → suppress HighLatency alerts
```

---

# 12. Secure Multi‑Account AWS CI/CD Architecture

Typical structure:

```
Dev Account
CI/CD Account
Shared Services
Production Account
```

Pipeline flow:

```
Developer → CI pipeline → Artifact store → AssumeRole → Production deploy
```

Benefits:

```
no developer production access
audit trail
controlled deployments
```

---

# 13. Artifact Signing

Purpose:

```
ensure artifact integrity
prevent tampering
verify trusted builds
```

Tools:

```
AWS Signer
cosign
Notary
GPG
```

Pipeline flow:

```
Build → Security Scan → Sign → Store → Verify → Deploy
```

---

# 14. Prevent Pipeline Bypass

Controls:

```
remove developer production permissions
deploy only via CI pipeline role
use cross‑account IAM roles
use SCP restrictions
use infrastructure as code
```

Example flow:

```
Developer → Git push
Pipeline builds artifact
Pipeline assumes production deploy role
Deployment occurs
```

Developers never receive production credentials.

---

# 15. Auditing Deployments

Monitoring stack:

```
AWS CloudTrail
CloudWatch
AWS Config
GuardDuty
```

Centralized architecture:

```
All accounts → CloudTrail logs → Security account
```

Alerts can trigger on:

```
unexpected AssumeRole
manual resource modification
deployment outside pipeline
```

---

# DevOps Troubleshooting Framework (Remember This)

Most DevOps interview debugging questions follow this pattern:

```
1. Identify the problem
2. Inspect logs
3. Check configuration
4. Verify infrastructure
5. Apply fix
```

If you answer problems using this structure, interviewers usually see it as **strong troubleshooting methodology**.

---

# Quick Interview Speaking Template

Use this structure when answering scenario questions:

```
1. Identify symptoms
2. Check logs and metrics
3. Inspect configuration
4. Validate infrastructure components
5. Apply remediation
```

This makes answers sound **structured and senior‑level**.

---

# Final Tip for Interview Day

For scenario questions:

```
Think → Structure → Answer
```

Avoid jumping straight to commands.

Interviewers value **structured reasoning more than memorized commands**.
