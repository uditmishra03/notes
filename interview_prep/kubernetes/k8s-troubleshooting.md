# Kubernetes Troubleshooting Interview Questions

---

## 1. CrashLoopBackOff Troubleshooting

### Meaning
Container repeatedly crashes and Kubernetes restarts it with exponential backoff.

### Investigation Steps
1. Check pod events  
```bash
kubectl describe pod <pod>
```

2. Check logs  
```bash
kubectl logs <pod>
kubectl logs <pod> --previous
```

3. Common Causes
- Application crash
- OOMKilled (memory limit exceeded)
- Wrong startup command
- Liveness probe failure
- Missing configuration or secrets

4. Verify
- resource requests/limits
- probe configuration
- environment variables/config maps

### Exit Code Reference

| Exit Code | Meaning                                 |
| --------- | --------------------------------------- |
| 0         | Success (but container shouldn't exit!) |
| 1         | Application error                       |
| 137       | SIGKILL (OOMKilled or manual kill)      |
| 139       | SIGSEGV (segmentation fault)            |
| 143       | SIGTERM (graceful shutdown)             |

---

## 2. OOMKilled Containers

### Cause
Container exceeded memory limit.

### How to Identify
```bash
kubectl describe pod <pod>
kubectl top pod <pod>
```

Example output:
```
Last State:     Terminated
  Reason:       OOMKilled
  Exit Code:    137
```

### Fix Options
1. Increase memory limits
2. Optimize application memory usage
3. For Java apps - configure JVM heap properly

```yaml
resources:
  requests:
    memory: "512Mi"
  limits:
    memory: "1Gi"
```

### Java Application Rule
```
Container limit = Xmx + 150Mi (for metaspace, stack, native memory)
```

---

## 3. Pod Stuck in Pending State

### Possible Reasons
- Insufficient node resources
- PVC not bound
- Node selector mismatch
- Namespace resource quotas hit

### Debug Commands
```bash
kubectl describe pod <pod>
kubectl get events
kubectl describe node <node>
```

---

## 4. ImagePullBackOff

### Causes
- Incorrect image name
- Registry authentication issue
- Image not found
- Network issue

### Debug
```bash
kubectl describe pod <pod>
# Look at Events section for pull errors
```

---

## 5. Application Not Accessible in Kubernetes

### Debug Flow
```
Client
↓
Load Balancer
↓
Ingress
↓
Service
↓
Pod
```

### Checks
- Load balancer health checks
- Ingress rules
- Service selector matches pod labels
- Service endpoints exist
- Pod is listening on correct port
- Security groups / network policies

---

## 6. Kubernetes DNS Troubleshooting

### Step 1 – Test DNS inside pod
```bash
kubectl run dns-test --image=busybox -it --rm -- sh
nslookup kubernetes.default
```

### Step 2 – Inspect pod DNS config
```bash
cat /etc/resolv.conf
```

Expected:
```
nameserver <coredns-ip>
search svc.cluster.local
```

### Step 3 – Verify CoreDNS
```bash
kubectl get pods -n kube-system
kubectl logs -n kube-system <coredns-pod>
```

### Step 4 – Check service
```bash
kubectl get svc -n kube-system
kubectl get endpoints kube-dns -n kube-system
```

---

## 7. Cluster Becomes Slow but Pods Healthy

### Debug Approach - Trace Request Path
```
Client
↓
Load Balancer
↓
Ingress
↓
Service
↓
Pod
↓
Dependencies
↓
Node resources
```

### Checks
- Load balancer latency
- Service endpoints
- DNS resolution (CoreDNS)
- Database or external API latency
- Node CPU / memory / disk IO

---

## 8. Quick Kubernetes Troubleshooting Commands

| Issue            | Command                                               |
| ---------------- | ----------------------------------------------------- |
| DNS resolution   | `nslookup kubernetes.default`                         |
| Pod DNS config   | `cat /etc/resolv.conf`                                |
| CoreDNS pods     | `kubectl get pods -n kube-system -l k8s-app=kube-dns` |
| CoreDNS logs     | `kubectl logs -n kube-system -l k8s-app=kube-dns`     |
| DNS service      | `kubectl get svc,ep kube-dns -n kube-system`          |
| Network policies | `kubectl get netpol -A`                               |
| Pod events       | `kubectl describe pod <pod>`                          |
| Previous logs    | `kubectl logs <pod> --previous`                       |

---

## 9. CrashLoopBackOff Causes Checklist

| Cause                      | How to Identify                             |
| -------------------------- | ------------------------------------------- |
| **Application bug**        | Check logs for stack traces                 |
| **Missing config**         | Check for ConfigMap/Secret errors in events |
| **OOMKilled**              | Exit code 137, check `kubectl describe pod` |
| **Liveness probe failing** | Events show "Liveness probe failed"         |
| **Missing dependencies**   | Logs show connection refused/timeout        |
| **Permission issues**      | Logs show "permission denied"               |
| **Image issues**           | Events show ImagePullBackOff first          |

---

## 10. What Happens When Running `kubectl apply`

### Flow
```
kubectl
↓
API Server
↓
Authentication
↓
Authorization
↓
Admission Controllers
↓
etcd (desired state stored)
↓
Scheduler selects node
↓
Kubelet creates container
↓
Status reported back to API server
```

Controllers ensure actual state matches desired state.

---

## 11. Debugging with Interactive Shell

```bash
# Override entrypoint to keep container running
kubectl run debug --image=<same-image> --rm -it --command -- /bin/sh

# Or modify deployment temporarily
# Change command to: ["sleep", "infinity"]
```

---

## 12. Network Policy Debugging

DNS requires:
- **UDP port 53** - standard DNS queries
- **TCP port 53** - large responses, zone transfers

Example allowing DNS traffic:
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
