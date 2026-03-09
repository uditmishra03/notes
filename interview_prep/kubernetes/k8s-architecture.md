# Kubernetes Architecture Interview Questions

---

## 1. HPA vs Cluster Autoscaler

| Feature | HPA                  | Cluster Autoscaler   |
| ------- | -------------------- | -------------------- |
| Scales  | Pods                 | Nodes                |
| Trigger | CPU / memory metrics | Unschedulable pods   |
| Purpose | Handle traffic load  | Add cluster capacity |

### HPA Example
Scale pods when CPU > 70%.

### Cluster Autoscaler
Adds new nodes when pods cannot be scheduled.

---

## 2. HPA vs VPA vs Cluster Autoscaler vs Karpenter

| Component          | What it scales | Trigger                    |
| ------------------ | -------------- | -------------------------- |
| HPA                | Pod replicas   | CPU/Memory metrics         |
| VPA                | Pod resources  | Resource usage analysis    |
| Cluster Autoscaler | Nodes          | Unschedulable pods         |
| Karpenter          | Nodes          | Unschedulable pods (faster)|

---

## 3. What Happens When a Kubernetes Deployment is Updated

### Expected Explanation
- Rolling update strategy
- New ReplicaSet creation
- Gradual pod replacement
- Old pods terminated after new pods ready

---

## 4. Kubernetes Service Discovery

### How it Works
- kube-dns / CoreDNS
- Service name resolution
- ClusterIP exposes internal IP

### DNS Format
```
<service-name>.<namespace>.svc.cluster.local
```

---

## 5. Docker Container vs Kubernetes Pod

### Docker Container
- Runtime instance of container image

### Kubernetes Pod
- Smallest deployable unit in Kubernetes
- Can contain one or multiple containers

### Key Characteristics
- Shared network namespace
- Shared storage volumes
- Same IP address for all containers in pod

---

## 6. Zero Downtime Deployment

### Rolling Update Strategy
Old pods gradually replaced by new pods.

```yaml
strategy:
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

### Key Components
- Deployment controller
- Readiness probes
- Multiple replicas

### Advanced Strategies
- Blue-Green deployment
- Canary deployment

---

## 7. Designing Highly Available Kubernetes Platform

### Control Plane
- Multiple API servers behind load balancer
- Multiple controller managers
- Multiple schedulers

### etcd
- 3 or 5 node etcd cluster
- Regular snapshots/backups

### Worker Nodes
- Nodes across multiple availability zones
- Cluster autoscaler / Karpenter

### Application Layer
- Multiple replicas
- Rolling updates
- Pod disruption budgets

### Configuration Management
- GitOps
- Version-controlled manifests

---

## 8. ConfigMap vs Secret

| Feature   | ConfigMap               | Secret                  |
| --------- | ----------------------- | ----------------------- |
| Data type | Non-sensitive config    | Sensitive data          |
| Encoding  | Plain text              | Base64 encoded          |
| Usage     | Env variables / volumes | Env variables / volumes |

---

## 9. StatefulSet vs Deployment

### Deployment
- Stateless applications
- Web servers / APIs
- Pods interchangeable

### StatefulSet
- Stateful applications
- Databases
- Stable network identity
- Persistent storage
- Ordered startup and termination

---

## 10. Managing Secrets in Kubernetes

### Kubernetes Secret
Stores sensitive data such as:
- DB passwords
- API keys
- Tokens

### Important Note
Secrets are **base64 encoded, not encrypted by default**.

### Best Practice
Use external secret managers:
- AWS Secrets Manager
- HashiCorp Vault
- GCP Secret Manager

---

## 11. Prevent Containers from Running as Root

### Pod Security Context
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

### Additional Controls
- Pod Security Standards
- OPA Gatekeeper
- Kyverno policies
- Admission controllers

---

## 12. Helm vs Raw Kubernetes YAML

### Problems Helm Solves
- Templating
- Versioning
- Environment configuration
- Release rollback

---

## 13. What Happens Internally When Running `kubectl apply`

### Flow
```
kubectl → API Server → Auth → Admission Controllers → etcd → Scheduler → Kubelet → Container Created
```

---

## 14. Kubernetes Ingress and Service Types

### Service Types
- **ClusterIP** - Internal only
- **NodePort** - Expose on node port
- **LoadBalancer** - Cloud provider LB

### Ingress
- L7 routing
- Host and path-based routing
- TLS termination

---

## 15. Pod Affinity and Anti-Affinity

### Use Cases
- Co-locate related pods (affinity)
- Spread pods across nodes (anti-affinity)
- High availability requirements

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector:
        matchLabels:
          app: web
      topologyKey: kubernetes.io/hostname
```
