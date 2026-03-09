Great idea. Having a **single revision sheet** is extremely useful before interviews.
I created a **clean markdown summary of all the questions we practiced**, with **short pointers instead of long paragraphs**, so you can quickly revise them.

---

```markdown
# DevOps / Kubernetes Interview Revision Notes

---

# 1. CI/CD Pipeline Architecture

## Key Points
- Git push triggers Jenkins pipeline via webhook.
- Shared libraries standardize pipeline logic across microservices.
- CI pipeline stages:
  - checkout
  - build
  - Docker image creation
  - SonarQube scan
  - security scan (BlackDuck/Trivy)
- PR builds run validation stages.
- Merge builds push image to artifact registry.

## Deployment
- Helm charts used for Kubernetes deployments.
- Deployment automated through Ansible playbooks.

## Key Concepts
- CI = build + test + security validation.
- CD = deployment automation.

---

# 2. Prevent Shared Library Changes from Breaking Pipelines

## Strategy
- Each microservice has its own pipeline.
- Shared library contains reusable pipeline logic.

## Safety Measures
- Version-controlled shared libraries.
- Feature branches for library changes.
- Regression testing before merge.
- Rollback to previous working version if needed.

---

# 3. CrashLoopBackOff Troubleshooting

## Meaning
Container repeatedly crashes and Kubernetes restarts it with exponential backoff.

## Investigation Steps
1. Check pod events  
```

kubectl describe pod <pod>

```

2. Check logs  
```

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

---

# 4. Application Not Accessible in Kubernetes

## Debug Flow
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

````

## Checks
- Load balancer health checks
- Ingress rules
- Service selector matches pod labels
- Service endpoints exist
- Pod is listening on correct port
- Security groups / network policies

---

# 5. Prevent Containers from Running as Root

## Pod Security Context

Example:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
````

## Additional Controls

* Pod Security Standards
* OPA Gatekeeper
* Kyverno policies
* Admission controllers

Purpose:
Prevent containers from running as root user.

---

# 6. HPA vs Cluster Autoscaler

| Feature | HPA                  | Cluster Autoscaler   |
| ------- | -------------------- | -------------------- |
| Scales  | Pods                 | Nodes                |
| Trigger | CPU / memory metrics | Unschedulable pods   |
| Purpose | Handle traffic load  | Add cluster capacity |

## HPA Example

Scale pods when CPU > 70%.

## Cluster Autoscaler

Adds new nodes when pods cannot be scheduled.

---

# 7. What Happens When Running `kubectl apply`

## Flow

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

# 8. Docker Container vs Kubernetes Pod

## Docker Container

* Runtime instance of container image.

## Kubernetes Pod

* Smallest deployable unit in Kubernetes.
* Can contain one or multiple containers.

## Key Characteristics

* Shared network
* Shared storage volumes
* Same IP address

---

# 9. Managing Secrets in Kubernetes

## Kubernetes Secret

Stores sensitive data such as:

* DB passwords
* API keys
* tokens

Example usage

* environment variables
* mounted volumes

## Important Note

Secrets are **base64 encoded, not encrypted by default**.

## Best Practice

Use external secret managers:

* AWS Secrets Manager
* HashiCorp Vault
* GCP Secret Manager

---

# 10. Zero Downtime Deployment

## Rolling Update Strategy

Old pods gradually replaced by new pods.

Example configuration:

```yaml
strategy:
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1
```

## Key Components

* Deployment controller
* Readiness probes
* Multiple replicas

Advanced strategies

* Blue-Green deployment
* Canary deployment

---

# 11. Cluster Becomes Slow but Pods Healthy

## Debug Approach

Trace request path:

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

## Checks

* Load balancer latency
* Service endpoints
* DNS resolution (CoreDNS)
* Database or external API latency
* Node CPU / memory / disk IO

---

# 12. Designing Highly Available Kubernetes Platform

## Control Plane

* Multiple API servers behind load balancer
* Multiple controller managers
* Multiple schedulers

## etcd

* 3 or 5 node etcd cluster
* regular snapshots/backups

## Worker Nodes

* nodes across multiple availability zones
* cluster autoscaler / Karpenter

## Application Layer

* multiple replicas
* rolling updates
* pod disruption budgets

## Configuration Management

* GitOps
* version-controlled manifests

---

# Quick Kubernetes Troubleshooting

## Pod Pending

Possible reasons

* insufficient node resources
* PVC not bound
* node selector mismatch
* namespace resource quotas

## ImagePullBackOff

Causes

* incorrect image name
* registry authentication issue
* image not found
* network issue

---

# ConfigMap vs Secret

| Feature   | ConfigMap               | Secret                  |
| --------- | ----------------------- | ----------------------- |
| Data type | Non-sensitive config    | Sensitive data          |
| Encoding  | Plain text              | Base64 encoded          |
| Usage     | Env variables / volumes | Env variables / volumes |

---

# StatefulSet vs Deployment

## Deployment

* Stateless applications
* Web servers / APIs
* Pods interchangeable

## StatefulSet

* Stateful applications
* Databases
* Stable network identity
* Persistent storage
* Ordered startup and termination

```

---

# How to Use This Before the Interview

Best way to revise:

1. **Read the pointers only** (not full answers).
2. **Explain each topic in your own words.**
3. Try to keep answers within **45–60 seconds**.

That matches real interview timing.

---

If you'd like, I can also create **one more extremely useful document** for you:

**“15 DevOps questions that appear in almost every L1 interview.”**

Preparing those usually covers **~80% of interview questions.**
```
