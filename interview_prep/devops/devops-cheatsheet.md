# DevOps Interview Cheatsheet

---

## 1. Zombie Processes Debugging (Linux)

### Key Concept
Zombie processes have finished execution but their parent process hasn't collected the exit status.

### Process States Reference

| State | Meaning               |
| ----- | --------------------- |
| R     | Running or runnable   |
| S     | Interruptible sleep   |
| D     | Uninterruptible sleep |
| T     | Stopped               |
| **Z** | **Zombie (defunct)**  |

### Detection
```bash
ps -eo pid,ppid,state,comm | awk '$3=="Z"'
```

### Extract Parent PIDs
```bash
ps -eo pid,ppid,state | awk '$3=="Z"{print $2}' | sort -u
```

### Restart Parent Service
```bash
systemctl status <pid>
systemctl restart <service>
```

---

## 2. Mapping PID to System Service

### Commands
```bash
systemctl status <pid>
```

or

```bash
cat /proc/<pid>/cgroup
```

Example output:
```
/system.slice/nginx.service
```

---

## 3. Prometheus Alerting Strategy

### Goal
Avoid alert fatigue

### Best Practices
- Severity labels
- Time windows
- Grouping
- Inhibition
- SLO alerts

### Example Rule
```yaml
alert: HighErrorRate
expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
for: 10m
```

---

## 4. Alertmanager Grouping

### Example
```yaml
route:
  group_by: ["alertname","service"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 3h
```

### Purpose
Combine multiple alerts into one notification

---

## 5. Alertmanager Inhibition

Suppress secondary alerts when a major alert fires.

### Example
```yaml
inhibit_rules:
- source_match:
    severity: critical
  target_match:
    severity: warning
  equal: ["service"]
```

Scenario: ServiceDown → suppress HighLatency alerts

---

## 6. Observability - Logs vs Metrics vs Traces

| Type    | Purpose              |
| ------- | -------------------- |
| Logs    | Events/messages      |
| Metrics | Numeric performance  |
| Traces  | Request path/latency |

---

## 7. How to Detect a Slow Microservice

### Expected Answer
- Prometheus metrics
- Latency dashboards
- Distributed tracing

---

## 8. Relational vs NoSQL Databases

| SQL                | NoSQL               |
| ------------------ | ------------------- |
| Structured schema  | Flexible schema     |
| ACID transactions  | Eventual consistency|
| Vertical scaling   | Horizontal scaling  |

---

## 9. Database Indexing

### Why Important
- Faster query retrieval
- Reduced full table scans
- Improved performance

---

## 10. Handling Disagreements (Dev vs Ops)

### Good Answer
- Use data to support decisions
- Encourage collaboration
- Focus on system reliability
- Blameless post-mortems

---

## 11. What Happens When You Type google.com

### Flow
1. DNS lookup
2. TCP handshake
3. TLS handshake (HTTPS)
4. HTTP request
5. Response from server
6. Browser renders page

---

## 12. Load Balancer vs Reverse Proxy vs API Gateway

| Component      | Purpose              |
| -------------- | -------------------- |
| Load Balancer  | Traffic distribution |
| Reverse Proxy  | Application routing  |
| API Gateway    | API management       |

---

## 13. DevOps Interview Focus Areas

Behind questions they test:
1. Do you understand DevOps architecture?
2. Can you troubleshoot production systems?
3. Can you communicate clearly with engineering teams?

---

## 14. Quick Interview Answer Pattern

### Structure
**Step 1** - Short answer (30 seconds)
**Step 2** - Example

### Example
**Short answer:** Jenkins shared libraries help standardize pipelines across microservices.

**Example:** In our case we use shared libraries where each microservice passes build commands, while the pipeline logic remains centralized.

---

## 15. Interview Evaluation Areas

| Area                     | What They Look For           |
| ------------------------ | ---------------------------- |
| CI/CD Architecture       | End-to-end understanding     |
| Pipeline troubleshooting | Systematic approach          |
| Shared libraries         | Code reuse knowledge         |
| Practical understanding  | Real production experience   |
